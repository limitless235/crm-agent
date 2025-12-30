-- Create a test user
-- Password: password123
INSERT INTO users (id, email, hashed_password, role) 
VALUES (
    '550e8400-e29b-41d4-a716-446655440000', 
    'test@example.com', 
    '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGGa31yy', 
    'user'
) ON CONFLICT (email) DO NOTHING;

-- Create a test admin user
-- Password: password123
INSERT INTO users (id, email, hashed_password, role) 
VALUES (
    '660e8400-e29b-41d4-a716-446655440000', 
    'admin@example.com', 
    '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGGa31yy', 
    'admin'
) ON CONFLICT (email) DO NOTHING;
