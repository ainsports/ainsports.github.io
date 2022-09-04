import json
import ffmpeg
import os
import shutil
import datetime 

def convertMillis(millis):
    seconds=int((millis/1000)%60)
    minutes=int((millis/(1000*60))%60)
    hours=int((millis/(1000*60*60))%24)
    return seconds, minutes, hours

def createFolder(folderPath):
    if os.path.exists(folderPath) ==  False:
        os.mkdir(folderPath)



def createSummaryWithFade(noOfVideos, outputSummaryFile, fileNamesStr, clipPeriod):
    fades= []
    afades = []
    duration = 1
    prev_offset = 0
    prev_aoffset = 0
    vfade = '[0]'
    afade = '[0:a]'
    for j in range(noOfVideos-1):
        offset = clipPeriod + prev_offset - duration - 0.1
        aoffset = clipPeriod + prev_aoffset - duration - 0.1

        videoFade = vfade+'['+str(j+1)+':v]xfade=transition=hrslice:duration='+ str(duration) +':offset='+str(offset)  
        afade_1 = afade+ '['+str(j+1)+':a]acrossfade=d=1'
        if j < noOfVideos-2:
            vfade = '[vfade'+str(j+1)+']'
            videoFade = videoFade + vfade
            afade = '[afade'+str(j+1)+']'
            afade_1 = afade_1 + afade
        else:
            videoFade = videoFade + ',format=yuv420p'

        fades.append(videoFade)
        afades.append(afade_1)
        prev_offset = offset
        prev_aoffset = aoffset

    fadeStr = ';'.join(fades)
    afadesStr = ';'.join(afades)


    cmd = 'ffmpeg \
     ' + fileNamesStr + ' \
    -filter_complex "' + fadeStr + ';' + afadesStr +'" -movflags +faststart '+ outputSummaryFile 



    os.system(cmd)

        
        
        
def generateSummaryVideo(time_stamp, output_path = "static/media", time_span = 2, thresh = 0.5):
    secondsBefore = time_span
    secondsAfter = time_span
    video_path = f"video-{time_stamp}.mp4"
    input_file_path = f"outputs/prediction-{time_stamp}.json"
    predictions = ''
    new_time_stamp  = datetime.datetime.now().strftime('%m_%d_%Y_%H_%M_%S')
    outputSummaryFile = os.path.join(output_path,f'summary-{new_time_stamp}.mp4')
    ## read from save file
    
    f = open(input_file_path)
    selectFilter = ''
    fileNamesStr = ''
    actionFileNames = os.path.join(output_path,'Filename.txt')
    allFiles = open(actionFileNames, 'w')
    i = 1
    with open(input_file_path, 'r') as input_file:
        predictions_file = json.load(input_file) 
        predictions = predictions_file['predictions']
        for action in predictions:
            if float(action['confidence']) < thresh:
                print('confidence is low ', action['confidence'])
                continue
            actionType = action['label']
            actionTime = action['gameTime'].replace('1 - ','') 
            milliseconds = int(action['position'])
            #####
            milliseconds_before = milliseconds - (secondsBefore * 1000)
            milliseconds_before = 0 if milliseconds_before < 0 else milliseconds_before  
            sec_before, mints_before, hours_before = convertMillis(milliseconds_before)
            sec_before, mints_before, hours_before = str(sec_before).zfill(2), str(mints_before).zfill(2), str(hours_before).zfill(2)
            startTime = hours_before + ':'+ mints_before + ':' +  sec_before  

            milliseconds_after = milliseconds + (secondsAfter * 1000)
            sec_after, mints_after, hours_after = convertMillis(milliseconds_after)
            sec_after, mints_after, hours_after = str(sec_after).zfill(2), str(mints_after).zfill(2), str(hours_after).zfill(2) 
            endTime = hours_after + ':'+ mints_after + ':' +  sec_after  
            #####
            outputFile = os.path.join(output_path, str(milliseconds) +".mp4")
            allFiles.write("file '"+str(milliseconds) +".mp4'" + "\n")
            #allFiles.write("file 'AinSportClip.mp4'" + "\n")
            fileNamesStr = fileNamesStr + " -i " + os.path.join(output_path,str(milliseconds) + ".mp4")
            
            cmd = "ffmpeg -y -i "+ str(video_path) + " -ss " + str(startTime) + " -to " + str(endTime) + " -c:v libx264 -crf 30 "+ outputFile
            #print(cmd)
            os.system(cmd)
            i = i + 1



        allFiles.close()    
        if i> 0:
           #outputFile     
           #outputSummaryFile
           #cmd = "ffmpeg -y -f concat -i " + actionFileNames + " -c copy " + outputSummaryFile
           
           #print(cmd)
           #os.system(cmd)
           createSummaryWithFade(i-1, outputSummaryFile, fileNamesStr, clipPeriod) 

    return "https://ainsports.eu.ngrok.io/"+outputSummaryFile
