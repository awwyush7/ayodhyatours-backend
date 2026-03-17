-- Contact Inquiries Table
CREATE TABLE IF NOT EXISTS contact_inquiries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    full_name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Bookings Table
CREATE TABLE IF NOT EXISTS bookings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    package_name TEXT NOT NULL,
    number_of_people INTEGER NOT NULL DEFAULT 1,
    preferred_date TEXT,
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'confirmed', 'completed', 'cancelled')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tour Packages Table
CREATE TABLE IF NOT EXISTS tour_packages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    duration TEXT NOT NULL,
    image_url TEXT,
    rating DECIMAL(2, 1) DEFAULT 4.5,
    highlights TEXT[],
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE contact_inquiries ENABLE ROW LEVEL SECURITY;
ALTER TABLE bookings ENABLE ROW LEVEL SECURITY;
ALTER TABLE tour_packages ENABLE ROW LEVEL SECURITY;

-- Policies for contact_inquiries
CREATE POLICY "Allow public to insert contact inquiries"
    ON contact_inquiries FOR INSERT
    WITH CHECK (true);

CREATE POLICY "Allow authenticated users to read contact inquiries"
    ON contact_inquiries FOR SELECT
    USING (auth.role() = 'authenticated');

-- Policies for bookings
CREATE POLICY "Allow public to insert bookings"
    ON bookings FOR INSERT
    WITH CHECK (true);

CREATE POLICY "Allow authenticated users to read bookings"
    ON bookings FOR SELECT
    USING (auth.role() = 'authenticated');

CREATE POLICY "Allow authenticated users to update bookings"
    ON bookings FOR UPDATE
    USING (auth.role() = 'authenticated');

-- Policies for tour_packages
CREATE POLICY "Allow public to read tour packages"
    ON tour_packages FOR SELECT
    USING (is_active = true);

CREATE POLICY "Allow authenticated users to manage tour packages"
    ON tour_packages FOR ALL
    USING (auth.role() = 'authenticated');

-- Insert sample tour packages
INSERT INTO tour_packages (name, description, price, duration, rating, highlights) VALUES
('Ram Mandir Darshan', 'Visit the magnificent Ram Mandir and experience divine blessings', 8999.00, '2 Days / 1 Night', 4.9, ARRAY['Ram Mandir Visit', 'Hanuman Garhi', 'Kanak Bhawan', 'Saryu Aarti']),
('Divine Ayodhya Yatra', 'Complete spiritual journey covering all major temples and ghats', 12999.00, '3 Days / 2 Nights', 4.8, ARRAY['All Major Temples', 'River Cruise', 'Local Heritage Tour', 'Accommodation']),
('Spiritual Awakening', 'Premium package with yoga, meditation, and cultural experiences', 19999.00, '5 Days / 4 Nights', 5.0, ARRAY['Complete Pilgrimage', 'Yoga Sessions', 'Cultural Programs', 'Premium Hotels']);
