## Zelf Hackathon (Backend)

### How data is coming from Third party API

Assuming, this third party API has lots of data of all type of social platforms. 
<br />

With a single API Key, user can request 60 times in each 5 min. We have 2 APIs, one is for fetching content & other is for author. In each content, we have author id,  by which we can call author API. So if we go syncronously, it would take much time. Why? For a single page (page=1/2/3 ...) content API call, assume there are n contents, assume n contents are having n distincts authors. so just after inserting one single content, there will be n author API call. so the author API call will block other operations. 

<br />

For future statistics work, we need some relation with Author & Social Content. Here the relation is, each content will have a author must. So this is a foreign key relation. I created two models: Author & SocialContent.

To make it faster we have to make independent both. So to get author details, we need author unique id which is in content details. So in a celery task queue, we will fetch social contents by page number & will ber inserting to db along with author. To create a author object, we need just author id which is present at content details data.

<br/>

In another celery task queue, we will take first 20 author ids, which data aren't fetched yet. We have a flag for that in model. That task queue will be responsible to get author details and save to db. So in that way, both are running in background & will not impact the system that much.

<br/> 

### Project Setup:

* Create your virtual environment
* Create a .env file. take idea about it values from 'sample.env' file
* Run migrations by python manage.py migrate & create a super user
* Start the server by: python manage.py runserver
* The task queue once started will run continuesly. Why? If there are new data, it automatically insert to DB. At this moment there are sleep for 5 sec when it's done to fetch all data.
* To start the celery run in a separate terminal: celery -A core worker -l info
* Open a new terminal. To push 2 tasks to queue by a management command: python manage.py fetch_content_author
* In celery terminal, you will see, data are fetching for both content and author


### API Doc:

#### Content List API
Endpoint: '/api/v1/contents'
Method: GET
Filter options with: author_id, author_username, main_text, platform

Example: 'http://localhost:8000/api/v1/contents?author_id=852208&author_username=fongkailuan&main_text=Drag Marble&platform=facebook'

##### Response (Example)
```json
{
    "count": 158,
    "next": "http://localhost:8000/api/v1/contents/?page=2",
    "previous": null,
    "results": [
        {
            "id": 247,
            "author": {
                "id": 167,
                "unique_id": "919301",
                "username": "stuffedddd"
            },
            "data": {
                "media": {
                    "urls": [
                        "https://nyc3.digitaloceanspaces.com/hellozelf/content/2686819e-aac6-434c-83db-ab02b541699c.jpg"
                    ],
                    "media_type": "IMAGE"
                },
                "stats": {
                    "digg_counts": {
                        "likes": {
                            "id": 2992,
                            "count": 119778
                        },
                        "views": {
                            "id": 2885,
                            "count": 2600000
                        },
                        "comments": {
                            "id": 2293,
                            "count": 199
                        }
                    }
                },
                "author": {
                    "id": 919301,
                    "username": "stuffedddd"
                },
                "context": {
                    "main_text": "@pizzahuteg",
                    "tag_count": 1,
                    "char_count": 11,
                    "token_count": 1
                },
                "unique_id": 1996096,
                "unique_uuid": "31fca27a-9d67-458d-8e60-5be49a7933db",
                "creation_info": {
                    "timestamp": "2023-05-12T13:41:53.019333Z",
                    "created_at": "2023-05-12T13:41:53.019333Z"
                },
                "origin_details": {
                    "origin_url": "https://instagram.com/p/CqiKhfMA0iu",
                    "origin_platform": "instagram"
                },
                "origin_unique_id": "CqiKhfMA0iu"
            }
        }
    ]
}
```

<br />

#### Content statistics API:
Endpoint: `/api/v1/statistics`
Query options: create_start, create_end, media_type, author_platform, content_char_count, hash_tag
Example : `localhost:8000/api/v1/statistics?create_start=2023-02-01&create_end=2023-04-30&media_type=VIDEO&author_platform=instagram&content_char_count=200&hash_tag=tiktokviral`

##### Response (Example)
```json
{
    "total_content": 9,
    "total_likes": 3805000,
    "total_comments": 18578,
    "total_views": 211400000,
    "avg_likes_per_content": 422777.77777777775,
    "avg_views_per_content": 23488888.888888888,
    "avg_comments_per_content": 2064.222222222222,
    "distinct_total_authors": 5,
    "mention_in_text_by_author": 0,
    "hash_tag_count": [
        0
    ]
}
```
