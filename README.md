Please follow the steps to run this Steller Prediction API
- Please download the zip code attached along with the model (LogisticRegression_Model.pkl)
- Make sure the docker is installed properly and running. I have implemented this on windows 10.
- Run the below command in the order as mentioned 

    - 1:  Build you docker using the blow command.
        - docker build -t flask .

        Desciption: This command will install all the libararies required to run this Flask api and also make a SQLlite table.

    - 2:  If you want to use the existing model present in the the directory, Please ignore this step else run the below command
        - python model.py

        Desciption: This will run the model and save a binary file to the current directory.

    - 3: Run the below command to run the docker
        - docker run -it -p 5000:5000 flask

        Description: This will run the api.
    
    - 4: Instead of the link mentioned on the console. Please open "Localhost:5000" on the browser to access the Flask API.
    
    - 5: You are ready to predict the steller classification.



    DEMO:





    

