### Action Spotting for Soccer Highlight Generation

This project deploys Action Spotting algorithms to localize the main actions of soccer games.

### What is Action Spotting?

Action Spotting is the task of localizing the moment specific actions occurs in an untrimmed video.
When applied to soccer videos, it enable the automatic retrieval of important actions happening during a game.

<p align="center">
    <img src="https://github.com/zaidalyafeai/Ain-Sports/raw/main/img/Abstract.png" width="480">
</p>


### Why it is important?

Localizing soccer actions in game enable the automatic generation of highlights. 
Generating highlights is usually time consuming, as the producer have to watch the full game to identify the main actions and decide which one to show in a highlight video. 
With an algorithm of action spotting, the producer already know when specific actions occur, hence only have to focus on the creative part of assembling which actions he deamed more suitable to show in the highlight.

### Algorithms for ACtion Spotting

The algorithm we deployed originate from [SoccerNet](https://www.soccer-net.org/).

In particular we are using [A Context-Aware Loss Function for Action Spotting in Soccer Videos (CALF)](https://openaccess.thecvf.com/content_CVPR_2020/papers/Cioppa_A_Context-Aware_Loss_Function_for_Action_Spotting_in_Soccer_Videos_CVPR_2020_paper.pdf), published at CVPR'20.
CALF localizes specific actions by learning the temporal context around the action.
More information on CALF, including its implementation, is available on [https://github.com/SoccerNet/sn-spotting](https://github.com/SoccerNet/sn-spotting/tree/main/Benchmarks/CALF).

<p align="center">
    <img src="https://github.com/zaidalyafeai/Ain-Sports/raw/main/img/Abstract-CALF.png" width="480">
</p>

### Test Sample 

<html>
    <script src="https://code.jquery.com/jquery-1.10.2.js"></script>
    <div id="a-placeholder"></div>
    <script>
        $(function(){
        $("#a-placeholder").load("sample.html");
        });
    </script>
</html>

### Live Demo 
<html>
    <script src="https://code.jquery.com/jquery-1.10.2.js"></script>
    <div id="b-placeholder"></div>
    <script>
        $(function(){
        $("#b-placeholder").load("upload.html");
        });
    </script>
</html>


### Project Developers

- [Zaid Alyafeai](https://github.com/zaidalyafeai/)
- [Silvio Giancola](https://github.com/silviogiancola/)
- [Anthony Cioppa](https://github.com/cioppaanthony/)
- [Abdullah Hamdi](https://github.com/ajhamdi/)
- [Hamzah Luqman](https://github.com/Hamzah-Luqman/)
