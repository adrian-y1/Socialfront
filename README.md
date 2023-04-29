# Socialfront

Visit website: [socialfront.up.railway.app](https://socialfront.up.railway.app/)

## Overview

SocialFront is a robust and feature-rich social networking application that has been built on the powerful Django web framework. The app is designed to emulate the core functionality of Twitter, enabling users to sign up, create a profile picture, follow other users, post tweets, like and comment on tweets, and browse through their own and others' timelines.

The app has been crafted with user experience and interface design in mind, ensuring that it is both intuitive and easy to use. The user interface is sleek and responsive, allowing users to effortlessly navigate through the app and quickly find the features they need.

This application was initially developed as a project for the "[CS50's Web Programming with Python and JavaScript course](https://cs50.harvard.edu/web/2020/)" course offered by Harvard University. Since then, it has undergone several enhancements and modifications to incorporate a wider range of features.

## Features

- User registration and login
- Reset password functionality with real email being sent
- Upload profile picture functionality
- Follow/unfollow functionality
- Ability to perform CRUD on posts
- Like and comment functionality on posts and comments
- View timelines for own and other users' posts
- Following/followers pages for each user
- DOM manipulations with JavaScript
- API endpoints for retrieving suggestions, followers, etc.

## Difficulties

During the development of the first version of this app, I encountered some challenges that I had to overcome. One of the biggest hurdles was implementing the edit function as well as the like/unlike button using JavaScript to manipulate the DOM. Since this required making AJAX calls to the API endpoints created in my views.py file, I had to learn how to use JavaScript's fetch method effectively. At the time, JavaScript, especially AJAX calls, were still relatively new to me, so it was challenging to figure out how to implement them.

One particular issue that I faced was with the edit function. After updating a post, if a user tried to edit another post, the edit post body form would have the same text as the previously edited post.

## Overcoming Challenges

As I was relatively new to AJAX calls, I faced several difficulties during the development of this app. To gain a better understanding of the topic, I used a range of online resources to start from the basics and gradually move towards more advanced concepts that i was working on. This allowed me to ensure that I fully comprehended every aspect of the process, and that I was not overlooking any crucial details.

In addition, I sought assistance from various Discord communities such as [CS50 discord](https://discord.gg/cs50) and [Programmer's Hangout discord](https://discord.gg/programming). This enabled me to receive feedback and suggestions on the issues I was facing, as well as the direction I was taking.

To overcome the issues i faced with the edit function's update post feature, I dug deep into my code and thoroughly debugged it, breaking down the problem to its root cause. I also utilized `console.log()` statements to identify the source of the issue and determine the best approach to tackle it.

## Conclusion

In conclusion, the development of this project was a challenging yet rewarding experience for me. As a beginner in JavaScript and AJAX calls, it was initially difficult to wrap my head around these concepts. However, I took the initiative to delve deeper into the workings of these technologies, and with perseverance and dedication, I was able to overcome the challenges I faced during the development process.

This project has not only equipped me with valuable knowledge and practical experience, but it has also helped me to apply the concepts I learned in this project to other projects I have worked on since then, such as [ChatNet](https://github.com/adrian-y1/ChatNet) or [Shopikart](https://github.com/adrian-y1/Shopikart).
