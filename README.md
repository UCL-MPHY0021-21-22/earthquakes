This exercise will look at how to read data from an online source (web service), explore and and process it.

You will work with a dataset describing earthquakes, provided by the [US Geological Survey](https://earthquake.usgs.gov/).
Your task will be to find the **location** and **magnitude** of the strongest earthquake in the UK in the last century.

You can find some initial code in the [earthquakes.py](./earthquakes.py) file, which you will need to complete.

## Step 0: Setup
Make sure you have read the note chapters on [working with files](http://github-pages.ucl.ac.uk/rsd-engineeringcourse/ch01data/060files.html), [Internet data](http://github-pages.ucl.ac.uk/rsd-engineeringcourse/ch01data/061internet.html) and [structured data files](http://github-pages.ucl.ac.uk/rsd-engineeringcourse/ch01data/064JsonYamlXML.html).

If you haven't already, fork this repository and clone it on your computer.

##  Step 1: Exploration
The dataset is in JSON format and can be downloaded from its source.
The `get_data` function shows how to retrieve the data. However, the function still needs some additions to make the data easier to work with!

1. Take a few moments to understand how we are requesting the data. What are the different parameters we provide? (you may want to look at the [documentation of the web service](https://earthquake.usgs.gov/fdsnws/event/1/) if you need help)
1. Explore the data to understand its structure (see suggestions below)
1. Complete the missing code in the function: how can you interpret the text retrieved, so that you can work with it in the code?

Before you start, take some time to understand the structure of the data. To see the data, you can try different things; for example:
- Get the response as shown in the code we've given you.
- Save the response body (`response.text`) in a text file (give the file a `.json` extension to help applications display it nicely!)
- Open the file in an editor like VS Code (you may want to [automatically format it](https://stackoverflow.com/questions/29973357/how-do-you-format-code-in-visual-studio-code-vscode) to make it look nicer). Some browsers may also display it so that the structure is clear.

The following questions may help you explore and understand how the data is laid out:
- How many broad "sections" does this response comprise?
- How many earthquakes are returned? (hint: is there any metadata included that could tell you this? How would you interpret it?) 
- One section (`"features"`) is by far larger than the others. How many entries does it hold?
- Pick one feature in this big list:
    - Can you see its location? Is that as a place name or coordinates?
    - Can you see its magnitude?
    - How do you think the time of the earthquake is represented?

## Step 2: Analysis
After the prevous step, your `get_data` function should return the information about the earthquakes.

Remember that your goal is to find the earthquake with the maximum magnitude and its location.
We have given you some suggestions of functions that you can use to work towards your solution. In this outline, the `get_maximum` function should return the magnitude and location; see the code at the end for how it should be used. 

Fill in the code for the remaining functions. Of course, you may come up with your own solution that uses a different structure.

There are two ways that you can run your program to check that it works and get the result:
- From the terminal, navigate to where it is stored and run `python earthquakes.py`
- From within VS Code, use the Run icon ("Run Python file in terminal"). Other IDEs may have a similar option.

If the program works, you should get a message with the location and magnitude of the strongest earthquake.