
const BASE_URL = 'http://localhost:8000/api';

type RequestOptions = {
    method?: string;
    headers?: Record<string, string>;
    body?: any;
};

export async function apiRequest(endpoint: string, options: RequestOptions = {}) {
    const { method = 'GET', headers = {}, body } = options;

    const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;

    const config: RequestInit = {
        method,
        headers: {
            'Content-Type': 'application/json',
            ...(token && { Authorization: `Bearer ${token}` }),
            ...headers,
        },
        ...(body && { body: JSON.stringify(body) }),
    };

    try {
        const response = await fetch(`${BASE_URL}${endpoint}`, config);

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || 'Something went wrong');
        }

        // Return null for 204 No Content
        if (response.status === 204) {
            return null;
        }

        return await response.json();
    } catch (error) {
        console.error('API Request Error:', error);
        throw error;
    }
}

export const auth = {
    login: (data: any) => {
        // Login expects form data for OAuth2 in the backend docs, but let's check if it accepts JSON too or if we need to send form data.
        // Docs say: "Request: Form data (OAuth2) - username, password"
        // So we need to send x-www-form-urlencoded
        const formData = new URLSearchParams();
        formData.append('username', data.username);
        formData.append('password', data.password);

        return fetch(`${BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: formData,
        }).then(async (res) => {
            if (!res.ok) throw new Error('Login failed');
            return res.json();
        });
    },
    signup: (data: any) => apiRequest('/auth/signup', { method: 'POST', body: data }),
    me: () => apiRequest('/users/me'),
};

export const gifts = {
    send: (data: any) => apiRequest('/gifts/', { method: 'POST', body: data }),
    sent: () => apiRequest('/gifts/sent'),
    received: () => apiRequest('/gifts/received'),
    details: (id: number) => apiRequest(`/gifts/${id}`),
};

export const friends = {
    list: () => apiRequest('/friends/'),
    request: (data: any) => apiRequest('/friends/request', { method: 'POST', body: data }),
    requests: () => apiRequest('/friends/requests/incoming'),
};

export const agent = {
    createSession: (data?: any) => apiRequest('/agent/sessions', { method: 'POST', body: data }),
    listSessions: () => apiRequest('/agent/sessions'),
    getSession: (id: string) => apiRequest(`/agent/sessions/${id}`),
    chat: (id: string, message: string) => apiRequest(`/agent/sessions/${id}/chat/sync`, { method: 'POST', body: { message } }),
    quickChaos: (data: any) => apiRequest('/agent/chaos-gift', { method: 'POST', body: data }),
};
