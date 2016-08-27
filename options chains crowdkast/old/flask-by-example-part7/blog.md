# Flask by Example - Updating the UI

In part 7 of this series, we'll work on the user interface to make it, well, more user friendly.

we’ll update the staging environment, with our latest code changes, by first setting up Redis on Heroku and then looking at how to run both our web and worker processes on a single dyno.

**Remember, here's what we're building: A Flask app that takes a URL and returns word-frequency pairs based on the text in the page's body.**

1. [Part One](http://www.realpython.com/blog/python/flask-by-example-part-1-project-setup): Setup a local development environment and then deploy both a staging environment and a production environment on Heroku.
1. [Part Two](http://www.realpython.com/blog/flask-by-example-part-2-postgres-sqlalchemy-and-alembic): Setup a PostgreSQL database along with SQLAlchemy and Alembic to handle migrations.
1. [Part Three](https://realpython.com/blog/python/flask-by-example-part-3-text-processing-with-requests-beautifulsoup-nltk/): Add in the back-end logic to scrape and then process the counting of words from a webpage using the requests, BeautifulSoup, and Natural Language Toolkit (NLTK) libraries.
1. [Part Four](https://realpython.com/blog/python/flask-by-example-implementing-a-redis-task-queue/): Implement a Redis task queue to handle the text processing.
1. [Part Five](https://realpython.com/blog/python/flask-by-example-integrating-flask-and-angularjs/): Setup Angular on the front-end to continuously poll the back-end to see if the request is done.
1. [Part Six](https://realpython.com/blog/python/updating-the-staging-environment/): Push to the staging server on Heroku - setting up Redis, detailing how to run two processes (web and worker) on a single Dyno.
1. **Part Seven: Update the front-end to make it more user-friendly. (current)**
1. Part Eight: Add the D3 library into the mix to graph a frequency distribution and histogram.
1. Part Nine: Add an Angular Service to the Module to clean up the code.
1. Part Ten: We'll look at unit and integration testing as well as a nice development workflow utilizing Continuous Integration and Delivery.

> Need the code? Grab it from the [repo](https://github.com/realpython/flask-by-example).

## Current User Interface

Let's look at the current user interface/experience.

Start Redis in terminal window:

```sh
$ redis-server
```

Then get your worker going in another window:

```sh
$ workon wordcounts
$ python worker.py
17:11:39 RQ worker started, version 0.4.6
17:11:39
17:11:39 *** Listening on default...
```

Finally, in a third window, fire up the app:

```sh
$ workon wordcounts
$ python manage.py runserver
```

Test the app out to make sure it still works. You should see something like:

![current user interface](link)

Let's make some changes.

1. We're going to disable the button to prevent users from continually clicking while they are waiting for the site to be counted.
1. Next we are going to display a Throbber where the wordcount list will go to show the user that there is an activity happening.
1. Finally we are going to display an error if the domain is unable to be reached.

## Changing the button

Change the button in the HTML to the following:

```html
{% raw %}
<button type="submit" class="btn btn-primary" ng-disabled="loading">{{ submitButtonText }}</button>
{% endraw %}
```

We add an `ng-disabled` [directive](https://docs.angularjs.org/api/ng/directive/ngDisabled) and attach that to `loading`. This will disable the button when `loading` evaluates to true. Next we add a variable to display to the user of `submitButtonText`. This way we'll be able to change the text from "Submit" to "Loading..." so the user knows what's going on. We then wrap the button in {% raw %} and {% endraw %} so that Jinja knows to evaluate this as raw HTML. If we don't do this Flask will try to evaluate the {{ submitButtonText }} as a Jinja variable and Angular won't get a chance to deal with/evaluate it.

The accompanying JavaScript is fairly simple.

At the top of the `WordcountController` add the following code:

```javascript
$scope.submitButtonText = "Submit";
$scope.loading = false;
```

This will initiate loading to false so that the button will not be disabled. It also initializes the button's text to be "Submit".

Change the post call to:

```javascript
$http.post('/start', {"url": userInput}).
  success(function(results) {
    $log.log(results);
    getWordCount(results);
    $scope.wordcounts = null;
    $scope.loading = true;
    $scope.submitButtonText = "Loading...";
  }).
  error(function(error) {
    $log.log(error);
  });
```

We add three lines, which set-

1. `wordcounts` to null so that old values get cleared out.
1. `loading` to `true` so that the loading button will be disabled via the `ng-disabled` directive we added to our HTML.
1. `submitButtonText` to "Loading..." so that the user knows why the button is disabled.

Next update the poller function:

```javascript
var poller = function() {
  // fire another request
  $http.get('/results/'+jobID).
    success(function(data, status, headers, config) {
      if(status === 202) {
        $log.log(data, status)
      } else if (status === 200){
        $log.log(data);
        $scope.loading = false;
        $scope.submitButtonText = "Submit";
        $scope.wordcounts = data;
        $timeout.cancel(timeout);
        return false;
      }
      // continue to call the poller() function every 2 seconds
      // until the timout is cancelled
      timeout = $timeout(poller, 2000);
    });
};
```

When the result is successful we set loading back to `false` so that the button is enabled again, and we change the button text back to "Submit" so the user knows they can submit a new URL.

Test it out!

## Adding a spinner

Next we want to add a spinner below our wordcount section so the user knows what's going on. This is accomplished by adding an animated gif img below the results div as shown below:

```html
<div id="results">
  <table class="table table-striped">
    <thead>
      <tr>
        <th>Word</th>
        <th>Count</th>
      </tr>
    </thead>
    <tbody>
    {% raw %}
      <tr ng-repeat="(key, val) in wordcounts">
        <td>{{key}}</td>
        <td>{{val}}</td>
      </tr>
  {% endraw %}
</div>
<img class="col-sm-3 col-sm-offset-4" src="/static/img/loader.gif" ng-show="loading">
```

You can see that `ng-show` is attached to loading just like the button is. This way when loading is set to true the spinner gif is shown. When loading is set to `false` (i.e., when the wordcount is finished) loading is set to `false` and the spinner dissapears.

## Dealing with errors

Finally we want to deal with the case where the user submits a bad URL, or some other error returned from the server. First, add the following HTML below the form:

```html
<div class="alert alert-danger" role="alert" ng-show='urlError'>
  <span class="glyphicon glyphicon-exclamation-sign" aria-hidden="true"></span>
  <span class="sr-only">Error:</span>
  There was an error submitting your URL. Please check to make sure it is valid before trying again.
</div>
```

This uses Bootstrap's `alert` [class](http://getbootstrap.com/components/#alerts) to show a warning dialog if the user submits a bad URL. We use angular's `ng-show` [directive](https://docs.angularjs.org/api/ng/directive/ngShow), similar to what we did with the spinner, to only show up when `urlError` is set to `true`.

Finally, in JavaScript we want to initialize `$scope.urlError` to `false` so the warning doesn't show up at the start.

```javascript
$scope.urlError = false;
```

We'll the catch errors in the `poller` function:

```js
var poller = function() {
  // fire another request
  $http.get('/results/'+jobID).
    success(function(data, status, headers, config) {
      if(status === 202) {
        $log.log(data, status);
      } else if (status === 200){
        $log.log(data);
        $scope.loading = false;
        $scope.submitButtonText = "Submit";
        $scope.wordcounts = data;
        $timeout.cancel(timeout);
        return false;
      }
      // continue to call the poller() function every 2 seconds
      // until the timout is cancelled
      timeout = $timeout(poller, 2000);
    }).
    error(function(error) {
      $log.log(error);
      $scope.loading = false;
      $scope.submitButtonText = "Submit";
      $scope.urlError = true;
    });
};
```
This logs the error to the console, changes `loading` to `flase`, sets the submit button's text back to "Submit" so that the user can try again, and changes `urlError` to `true` so that the warning shows up.

Lastly, in our `success` function for the post call we want to set `urlError` to `false` so that it dissapears when the user tries to submit a new url:

```javascript
$scope.urlError = false;
```

With that we've cleaned up the user interface a bit so that the user knows what is happening while we are running the wordcount functinality behind the scenes.