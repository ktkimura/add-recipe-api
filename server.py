import json, time, os
from recipe_scrapers import scrape_html

commFilePath = 'commPipe.json'

def fileChange(file):
    lastEditTime= os.path.getmtime(file)
    while True:
        newEditTime = os.path.getmtime(file)
        if lastEditTime != newEditTime:
            return 1


def getRecipeDetails(recipeLink):
    scraper = scrape_html(html=None, org_url=recipeLink, online=True);

    recipeName = scraper.title()
    recipeIngredients = scraper.ingredients()
    recipeInstruct = scraper.instructions()

    recipeObj = {"name":  recipeName,  "ingredients": recipeIngredients, "instructions": recipeInstruct}
    return recipeObj


while True:
    print("waiting for input")
    if fileChange(commFilePath) == 1:
        with open(commFilePath, 'r') as inputFile:
            time.sleep(1)

            # parse out the hyperlink
            fileData = json.load(inputFile)
            recipeLink = fileData["link"]
            
            inputFile.close()
        
        with open(commFilePath, 'w') as outputFile:

            # use recipe-scrapers library to get name, ingredients, and instructions
            rawRecipeObj = getRecipeDetails(recipeLink)
            json.dump(rawRecipeObj, outputFile, indent=4)

            outputFile.close()

