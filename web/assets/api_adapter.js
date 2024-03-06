/**
 * APIAdapter class to facilitate API calls.
 * This class automatically handles different environments, methods, and standard error responses.
 */
class APIAdapter {
    /**
     * Create an APIAdapter instance for a specific service.
     * 
     * @param {string} service - The service name, like 'user' or 'data'.
     */
    constructor(service) {
        this.service = service;
        this.environment = this.detectEnvironment();
    }

    /**
     * Detect the current environment based on the hostname.
     * 
     * @returns {string} - 'local', 'test', or 'production'
     */
    detectEnvironment() {
        if (window.location.hostname === 'localhost') {
            return 'local';
        } else if (window.location.hostname.endsWith('tst.example.com')) {
            return 'test';
        } else {
            return 'production';
        }
    }

    /**
     * Generate the base URL for API calls based on the environment.
     * 
     * @returns {string} - The base URL.
     */
    getBaseURL() {
        return `http://localhost:8080`;
        if (this.environment === 'local') {
            return `http://localhost:8084/${this.service}/`;
        } else if (this.environment === 'test') {
            return `https://${this.service}.tst.example.com/`;
        } else {
            return `https://${this.service}.example.com/`;
        }
    }

    /**
     * Make an API request.
     * 
     * @param {string} endpoint - API endpoint with optional templated sections like ':id'.
     * @param {string} method - HTTP method ('GET', 'POST', etc.)
     * @param {object} [payload=null] - Data to send with 'POST', 'PATCH', 'PUT', or 'QUERY'.
     * @param {string} [returnType='json'] - Expected return type ('json', 'csv', 'parquet').
     * @param {object} [params=null] - Object to replace templated sections in the endpoint.
     * @param {object} [queryString=null] - Object representing query string parameters.
     * @returns {Promise} - Promise resolving to the API response.
     */
    async makeRequest(endpoint, method, payload = null, returnType = 'text', params = null, queryString = null) {
        let templatedEndpoint = endpoint;
        if (params) {
            for (const [key, value] of Object.entries(params)) {
                templatedEndpoint = templatedEndpoint.replace(`:${key}`, value);
            }
        }
        
        let url = `${this.getBaseURL()}${templatedEndpoint}`;
  
        if (queryString) {
            const queryParams = new URLSearchParams(queryString).toString();
            url = `${url}?${queryParams}`;
        }

        let options = {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
        };

        if (['POST', 'PATCH', 'PUT', 'QUERY'].includes(method)) {
            options.body = JSON.stringify(payload);
        }

        const response = await fetch(url, options);

        if (response.status === 401) {
            window.location.href = '/sign-in';
            return;
        }

        if ([403, 500, 518, 522, 527].includes(response.status)) {
            const error = new Error(`HTTP Error: ${response.status}`);
            error.statusCode = response.status;
            throw error;
        }

        if (returnType === 'json') {
            return await response.json();
        } else if (returnType === 'text') {
            return await response.text();
        } else if (returnType === 'parquet') {
            return await response.arrayBuffer();
        } else {
            throw new Error(`Unsupported return type: ${returnType}`);
        }
    }

    /**
     * Perform a GET request.
     * @param {string} endpoint - The API endpoint.
     * @param {object} [params=null] - Object to replace templated sections in the endpoint.
     * @param {object} [queryString=null] - Object representing query string parameters.
     */
    async get(endpoint, params = null, queryString = null) {
        return await this.makeRequest(endpoint, 'GET', null, 'json', params, queryString);
    }

    /**
     * Perform a POST request.
     *
     * @param {string} endpoint - The API endpoint
     * @param {object} payload - Data to send
     * @param {string} [returnType='json'] - Expected return type ('json', 'csv', 'parquet')
     */
    async post(endpoint, payload, returnType = 'json') {
        return await this.makeRequest(endpoint, 'POST', payload, returnType);
    }

    /**
     * Perform a custom QUERY request.
     *
     * @param {string} endpoint - The API endpoint
     * @param {object} payload - Data to send
     * @param {string} [returnType='json'] - Expected return type ('json', 'csv', 'parquet')
     */
    async query(endpoint, payload, returnType = 'json') {
        return await this.makeRequest(endpoint, 'POST', payload, returnType);
    }

    /**
     * Perform a DELETE request.
     * @param {string} endpoint - The API endpoint.
     */
    async delete(endpoint) {
        return await this.makeRequest(endpoint, 'DELETE');
    }

    /**
     * Perform a PATCH request.
     * @param {string} endpoint - The API endpoint.
     * @param {object} payload - Data to send.
     */
    async patch(endpoint, payload) {
        return await this.makeRequest(endpoint, 'PATCH', payload, 'json');
    }

    /**
     * Perform a PUT request.
     * @param {string} endpoint - The API endpoint.
     * @param {object} payload - Data to send.
     */
    async put(endpoint, payload) {
        return await this.makeRequest(endpoint, 'PUT', payload, 'json');
    }

}

