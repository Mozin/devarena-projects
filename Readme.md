# Test Project

Created by Mohsin Vindhani

### Introduction

This repository contains the code for the API developed as a part of Screening Process

### Main Technologies used

* Flask
* PostgresSQL


### Error Messages

For All the endpoints, a JSON validation is done first followed by the verification of various business rules. 
The output error message for all the endpoints is in a form of a predefined 
codes like `USER_NOT_FOUND`, `PROJECT_NOT_FOUND`. The list of all possible error messages on 
an endpoint is displayed in the Swagger documentation