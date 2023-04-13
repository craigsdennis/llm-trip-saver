def get_profile_api_docs(company):
    return f"""API documentation:
        Endpoint: https://llm-companies.cyclic.app/api/{company}
        GET /profiles

        This API is for searching user profiles

        Query parameters table:
        id | integer | Retrieves the unique identifier for a specific user. A valid vaule should be an integer between 1 and 1000 | optional
        email | string | The email address of a specific user. | optional
        _limit | integer | The maximum number of profiles per page. A valid value should be an integer between 1 and 10 (inclusive). default: 3 | optional

        Response schema (JSON object):
        id | integer | required
        first_name | string | required
        last_name | string | required
        email | string | required

        Use _limit: 1
        """