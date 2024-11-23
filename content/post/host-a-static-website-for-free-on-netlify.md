---
title: "Host a Static Website for Free on Netlify"
date: 2024-11-10
draft: false
tags: ["markdown", "tutorial", "hugo", "blog"]
image: "/img/posts/img-4.jpg"
Description: "Let me explain this guide for hosting a website on Netlify in simpler terms:"
featured: true
---
# Hosting Your Hugo Website for Free on Netlify

## What is Netlify?
Netlify is like a free hosting service for your website - think of it as a place that makes your website available to everyone on the internet. It's especially good for static websites (like those built with Hugo) because:
- It's completely free for basic use
- It's very fast
- It's easy to set up
- It automatically updates your site when you make changes

## Setting Up Your Site on Netlify

### Step 1: Prepare Your Configuration
Create a file called `netlify.toml` in your main project folder. This file tells Netlify how to handle your website:

```toml
[build]
publish = "public"          # This tells Netlify where your finished website files are
command = "hugo --gc --minify"  # This tells Netlify to use Hugo to build your site

# Settings for your main website
[context.production.environment]
HUGO_VERSION = "0.82.0"    # Specifies which version of Hugo to use
HUGO_ENV = "production"    # Tells Hugo this is for your live website
HUGO_ENABLEGITINFO = "true"  # Allows Hugo to use Git information

# Settings for different deployment scenarios
[context.split1]
command = "hugo --gc --minify --enableGitInfo"

[context.split1.environment]
HUGO_VERSION = "0.82.0"
HUGO_ENV = "production"

# Settings for preview deployments (when you want to test changes)
[context.deploy-preview]
command = "hugo --gc --minify --buildFuture -b $DEPLOY_PRIME_URL"

[context.deploy-preview.environment]
HUGO_VERSION = "0.82.0"

# Settings for branch deployments
[context.branch-deploy]
command = "hugo -b $DEPLOY_PRIME_URL"

[context.branch-deploy.environment]
HUGO_VERSION = "0.82.0"

[context.next.environment]
HUGO_ENABLEGITINFO = "true"
```

### Step 2: Choose Your Deployment Method

You have two ways to get your website onto Netlify:

#### Option 1: Direct Upload
1. Build your Hugo site locally (run `hugo` command)
2. Go to Netlify's website
3. Sign up or log in
4. Drag and drop your `public` folder onto Netlify's dashboard
5. Your site is live!

#### Option 2: GitHub Integration (Recommended)
1. Put your Hugo site on GitHub
2. Log in to Netlify
3. Click "New site from Git"
4. Choose GitHub and select your repository
5. Netlify will automatically:
   - Build your site whenever you update GitHub
   - Deploy your changes
   - Handle all the technical details

### Step 3: Custom Domain (Optional)
- Netlify gives you a free domain like `your-site-name.netlify.app`
- You can add your own custom domain through Netlify's settings
- Netlify even provides free HTTPS certificates

## Tips for Success
- Always test your site locally before pushing to GitHub
- Make sure your Hugo version in `netlify.toml` matches the version you use locally
- Keep your `public` folder in your `.gitignore` file if using GitHub
- Use Netlify's deploy previews to check changes before they go live

## Common Issues and Solutions
1. **Build Fails**
   - Check your Hugo version matches netlify.toml
   - Make sure all your theme files are included
   
2. **Images Not Showing**
   - Check your image paths are correct
   - Make sure images are in the static folder

3. **Deployment Stuck**
   - Check your repository permissions
   - Verify your build settings in netlify.toml

Need help? Check Netlify's documentation or their community forums for support!
