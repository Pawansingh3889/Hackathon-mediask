# Google OAuth Setup and Deployment

## Introduction
Google OAuth is a secure authorization protocol that allows applications to obtain limited access to user accounts on an HTTP service. This documentation will guide you through the setup and deployment of Google OAuth in the Hackathon-mediask repository.

## Prerequisites
- **Tools Needed**: 
  - Google Developer Account
  - Node.js or another server-side environment
  - A version control system (e.g., Git)
- **Libraries/Frameworks**: 
  - Express or similar web frameworks
  - Passport.js or any relevant OAuth library

## Setting Up Google OAuth

### Step 1: Creating a Google Developer Account
1. Go to the [Google Developer Console](https://console.developers.google.com/).
2. Sign in or create a new account.

### Step 2: Creating a New Project
1. Click on the project dropdown at the top of the page and select "New Project."
2. Enter a name for your project and click "Create."

### Step 3: Configuring OAuth Consent Screen
1. Go to the "OAuth consent screen" tab.
2. Provide application details such as name, logo, and support email.

### Step 4: Creating OAuth Credentials
1. Navigate to the "Credentials" menu.
2. Click on "Create Credentials" and select "OAuth 2.0 Client IDs."
3. Set the application type (Web application) and provide the necessary redirect URIs.
4. Note down the Client ID and Client Secret.

## Integrating Google OAuth into the Project

### Installing Necessary Libraries
Run the following command to install the required libraries (Node.js example):
```bash
npm install passport-google-oauth20 express-session
```

### Implementing OAuth
```javascript
const GoogleStrategy = require('passport-google-oauth20').Strategy;
const passport = require('passport');

passport.use(new GoogleStrategy({
    clientID: process.env.GOOGLE_CLIENT_ID,
    clientSecret: process.env.GOOGLE_CLIENT_SECRET,
    callbackURL: "/auth/google/callback"
  },
  function(accessToken, refreshToken, profile, done) {
    // User authentication logic here
    done(null, profile);
  }
));

// Add redirect URIs to handle authentication
```

## Testing the Setup
1. Run your application locally.
2. Navigate to the OAuth URL you set up to initiate the login.
3. Ensure you can log in and obtain user information.

## Deployment

### Preparing for Deployment
1. Ensure all environment variables are set (Client ID, Client Secret).
2. Test locally to make sure everything is functioning.

### Deploying to a Hosting Platform
Follow the deployment instructions specific to your chosen platform (e.g., Heroku, Vercel). Update the Redirect URIs as required for the live environment.

## Conclusion
This guide walked you through the complete setup and deployment of Google OAuth in your Hackathon-mediask project. For further assistance, consult the [Google OAuth Documentation](https://developers.google.com/identity/protocols/oauth2).