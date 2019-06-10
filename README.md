# Lipstick Recommender

The goal of the project is to help customers discover different lipstick products, and give them recommendations about new lipstick shades they may like.

The repository contains a basic template for a Flask configuration that will work on Heroku.

The final web application can be found [here](https://get-your-lipsticks.herokuapp.com/)

More detail of how the code work can be found in `project_details.pptx`

## Step 1: Sephora web scraping 
- Run `Sephora_scraping.py`
- Run  `get_hot_shade.py` 
- Then you will get two .csv files containing product information and customer reviews.

## Step 2: Recommender
- Run `Recommender.py`. It will output the lipstick recommendations based on the input information. 

## More...
`Procfile`, `requirements.txt`, `conda-requirements.txt`, and `runtime.txt`
  contain some default settings.
- There is some boilerplate HTML in `templates/`
- Create Heroku application with `heroku create <app_name>` or leave blank to
  auto-generate a name.


