import json
import ffmpeg
import os
import shutil

def convertMillis(millis):
    seconds=int((millis/1000)%60)
    minutes=int((millis/(1000*60))%60)
    hours=int((millis/(1000*60*60))%24)
    return seconds, minutes, hours

def createFolder(folderPath):
    if os.path.exists(folderPath) ==  False:
        os.mkdir(folderPath)

def generateSummaryVideo(video_path = 'video.mp4', prediction_file = "outputs/Predictions-v2.json",
                         output_path = "static/media", time_span = 2, thresh = 0.5):
    secondsBefore = time_span
    secondsAfter = time_span
    input_file_path = prediction_file
    predictions = ''

    outputSummaryFile = os.path.join(output_path,'summary.mp4')
    ## read from save file
    
    f = open(input_file_path)
    selectFilter = ''
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
            
            cmd = "ffmpeg -y -i "+ str(video_path) + " -ss " + str(startTime) + " -to " + str(endTime) + " -c:v libx264 -crf 30 "+ outputFile
            #print(cmd)
            os.system(cmd)
            i = i + 1



        allFiles.close()    
        if i> 0:
           #outputFile     
           #outputSummaryFile
           cmd = "ffmpeg -y -f concat -i " + actionFileNames + " -c copy " + outputSummaryFile
           
           #print(cmd)
           os.system(cmd)

    return "https://ainsports.eu.ngrok.io/"+outputSummaryFile
