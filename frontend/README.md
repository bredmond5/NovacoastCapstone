# DNS Twist

This is the React front-end for the DNS Twist application. 

## Dependencies

1. Install an IDE, preferably [VSCode](https://code.visualstudio.com/download).
    > You can use netbeans, but I can't help you if you have trouble with it.

2. Install [Docker](https://docs.docker.com/get-started/).
    > This is for making and running the containerized application.

## Start

1. Navigate to the **dns-twist-react** folder

2. To start run the command: `docker-compose up`

3. To stop run: `docker-compose down`

## Folder Structure

- ### /public
    - */public holds all of the files that are okay to be accessed by anyone visiting our site*
    - /assets   
        - holds all of our public assets like images and favicons
    - index.html
        - our only html document
        - this is the starting point for all react projects
    - manifest.json
        - settings for users who download our site to their device as a pwa
    - robots.txt
        - file for site crawlers, useful for seo

- ### /src
    - */src holds all of the react files that will be included in the diffing algorithm*
    - *must include all css and js files or webpack won't see them*
    - /components
        - this folder is where we put all of our react components
        - organizing this is by preference, I generally make subfolders by page if I know it's going to be a bigger project
        - bulk of the work is done here
    - index.js
        - renders everything in App.js to our index.html file
        - usually doesn't need touching
    - App.js
        - the root of our application
        - try to keep this as clean and comprehensive as possible
        - generally holds the router and context

## Resources
 - [React Docs](https://reactjs.org/docs/getting-started.html)
 - [React Router](https://reactrouter.com/web/guides/quick-start)
 - [Baseweb](https://baseweb.design/)
 - [Sass](https://sass-lang.com/guide)
 - [Docker](https://docs.docker.com/)
 - [Create React App](https://github.com/facebook/create-react-app)
 