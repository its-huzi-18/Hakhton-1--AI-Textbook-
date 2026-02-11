/**
 * Test script to verify the connection between frontend and backend
 */

async function testBackendConnection() {
    console.log('Testing backend connection...');
    
    // Use the same logic as in the frontend
    const backendUrl = window.BACKEND_ORIGIN|| 'http://localhost:8000';
    console.log(`Using backend URL: ${backendUrl}`);
    
    try {
        // Test the health endpoint first
        const healthResponse = await fetch(`${backendUrl}/health`);
        if (healthResponse.ok) {
            const healthData = await healthResponse.json();
            console.log('Backend health check passed:', healthData);
        } else {
            console.log('Backend health check failed:', healthResponse.status);
        }
        
        // Test the root endpoint
        const rootResponse = await fetch(`${backendUrl}/`);
        if (rootResponse.ok) {
            const rootData = await rootResponse.json();
            console.log('Backend root endpoint accessible:', rootData);
        } else {
            console.log('Backend root endpoint not accessible:', rootResponse.status);
        }
        
        console.log('Backend connection test completed.');
    } catch (error) {
        console.error('Error connecting to backend:', error.message);
    }
}

// For use in browser environment
if (typeof window !== 'undefined') {
    // Wait for the page to load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', testBackendConnection);
    } else {
        testBackendConnection();
    }
}

// For Node.js environment (would need to be adapted)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { testBackendConnection };
}