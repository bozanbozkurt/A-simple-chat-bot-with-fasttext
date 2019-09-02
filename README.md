# A-simple-chat-bot-with-fasttext

Bots are essential for modern chat services. Text classification is the main tool for giving automated answers or answer suggestions. The big problem with text classification are answeing multiple languages with the same system. Luckily with fasttext we can create bots for every language. Here is a simple training and answering tool that works with every common language since fasttext is character based.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

You will need python 3.6 or higher. pip3 is also neccessary.

```
pip3 install fasttext
pip3 install flask
pip3 install requests
```

### Installing

Run server.py on your local. 

```
python3 server.py
```

Now check your localhost.

```
http://localhost/demo
```

End with an example of getting some data out of the system or using it for a little demo

## Test

In order to test the system, we first need to train our model with some data. 

### Train

Copy the text on [sampleTurkish.json](sampleTurkish.md) and paste it on the FAQ area. 
Enter 2000 as epoch and 20 as word vector size. 
Hit the train button. 
You will see "training completed" in a while. 

### Query

Now you can test your bot. 
Enter a query and click on test. 
Server should respond with a json as below. 

```
[{
"predName":"__label__QnA0",
"score":0.9986332654953003,
"className":"1101xxxxxxbexx1"
},
{
"predName":"__label__QnA46",
"score":0.00092932244297117,
"className":"NotFound",
"classActual":"1101xxxxxxbexx6"
},
{
"predName":"__label__QnA3",
"score":0.0002752315194811672,
"className":"NotFound",
"classActual":"1101xxxxxxbexx4"
}]
```

If you look at the responses above, you will see the best result first. The classnames come from the sample data. 

## Important Notes

Fasttext performs better with an extra NotFound class, having a huge number of arbitrary sentences. 
If a class has less than 0.45 accurracy, we  accept it as ununderstood and the program returns NotFound className. 
Threshold parameter can be updated in the code. 

## Deployment

Fasttext supports Ubuntu, we recommend using it as it is hard to get fasttext running on other systems. 

## Built With

* [flask](https://flask.palletsprojects.com/en/1.1.x/) - Web Framework
* [pip](https://pypi.org/project/pip/) - Dependency Management
* [fasttext](https://fasttext.cc/) - Classification Library

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **B Ozan Bozkurt** - *Initial work* - [bozanbozkurt](https://github.com/bozanbozkurt)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Special thanks to SOR'UN team in creating sample data. 