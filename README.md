# COVID19-Assistant
## WORKING
The idea behind this project is to use a switch (doorbell) interfaced with Raspberry Pi, which when clicked triggers python scripts for `Face-Mask Detection` and `Social-Distance Detection`.
The scripts validate conditions (outside) through a camera and send results to Amazon S3. Now, a user can use the Alexa App / Amazon Echo to get information regarding COVID-19 parameters
outside. This is done by integrating AWS Lambda functions and Alexa Skills Kit (Developer Console).
<br>
<br>
Sample utterances: `Alexa is the person wearing a mask?` , `Alexa what is the situation outside?`.
<br>
## FLOW
<br>
<p align="center">
  <img src="https://user-images.githubusercontent.com/59433969/106308497-cc708d00-6286-11eb-8cc6-afcf27c50dbe.png" />
</p>

## SAMPLE OUTPUT
<br>
<p align="center">
<img src="https://user-images.githubusercontent.com/59433969/106309256-de066480-6287-11eb-823e-64fd9d9ab7ae.png" />
</p>
