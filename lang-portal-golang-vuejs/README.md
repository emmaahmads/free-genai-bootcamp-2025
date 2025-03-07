<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" class="logo" width="120"/>

# 

---

## Backend API Implementation

The Lang Portal backend is built using **Go** as the programming language and **Gin** as the web framework. It utilizes **PostgreSQL** for data storage and maintains organization by separating sections for handling API requests, database interactions, and SQL updates. **sqlc** is used for generating database queries.

### Key Features:

- **API Endpoints**: The API includes endpoints similar to Andrew's for language learning, covering words, groups, study sessions, and activities. These endpoints follow standard RESTful API rules.
- **Database Structure**: The database contains tables for:
    - Malay words with English translations and Jawi script.
    - Word groups.
    - Study activities.
    - Study sessions.
    - Word reviews.
- **Testing**: Unit tests are implemented for each endpoint, adhering to standard Go API backend practices.


## Frontend API Implementation

The frontend of the Lang Portal is developed using **Vue.js 3** and the **Composition API**. The interface is designed to be clean and user-friendly.

### Key Features:

- **Dashboard**: Displays important study statistics such as streaks and success rates, allowing users to easily navigate to different study activities.
- **Navigation**: Utilizes **Vue Router** for seamless navigation between views.
- **API Calls**: Employs **Axios** for making API calls to the backend.
- **Component Organization**: UI components are neatly organized into separate files for elements like:
    - Dashboard.
    - StudyActivities.
    - QuickStats.
- **Layout**: Features a grid-based dashboard with stat cards for quick progress updates and a card-based study activities page with pagination for easy browsing.


### Future Development:

The frontend is still a work in progress. Future plans include enhancing the user experience to make language learning more enjoyable and engaging.

