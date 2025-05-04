# IPL Prediction Project

## Project structure

### backend 
* Django rest framework is used in backend.
* to run the backend api -
```
cd backend
docker-compose up --build
```

### Info about backend
* backend contains IPL current match prediction ML model `IPL_SCORE_WINNER_PREDICTION_MODEL`.
* To see current date's matches predictions - go to -> `http://127.0.0.1:8000/api/current-predictions/`. In current matches I have used `groq` LLM for analysis of the predictions.
(used groq's api due to my system capabalitites to not be able to run Ollama models locally that easily)
* `current-predictions` api endpoint only shows predictions of the current date's matches not previous.


I have also create an `http://127.0.0.1:8000/api/upload-matches/` endpoint to upload the scrapped `latest matches lineup` and the current teams `home and away` winrates to the database which will be used for predictions. After storing in the database it shows users all the matches. 

* IPL Match winner prediction model is trained on `ipl_2024_matches.csv` data which contains all the IPL matches details of year 2024
* The `ipl_2024_deliveries.csv` file contains every matches ball by ball data which is also used to extract necessary features for training our model.


## Still working on the frontend...
