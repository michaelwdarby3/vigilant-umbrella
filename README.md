# vigilant-umbrella


To start, install the python packages required in requirements.txt, in an environment with a valid Python installation, by running the command

$ pip install -r requirements.txt

Once the installation finishes (it involves a tensorflow installation, so may take up to 10 minutes), to run the program, run

$ python main.py

It will start up a flask application and initialize the model.  This should take a couple of minutes. Once it's started, on your browser, navigate to "http://127.0.0.1:5000/recommendations?user_id=2bc424123e0a12d29c488bb6e565fe98d0a49b46", where the argument for user_id can be any of the user_ids in the dataset. It will return a json to you after a couple of seconds.
