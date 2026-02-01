import { createClient } from "https://cdn.jsdelivr.net/npm/@supabase/supabase-js/+esm";

// ✅ CORRECT Supabase Project URL (NO extra letters)
export const SUPABASE_URL = "https://bmkqsacuqyiekusmaztf.supabase.co";

// ✅ Correct publishable / anon key
export const SUPABASE_ANON_KEY = "sb_publishable_wfzTtdAhw0K2yXLXcRKVWw_8z5p4rwN";

// ✅ Create Supabase client
export const supabase = createClient(
  SUPABASE_URL,
  SUPABASE_ANON_KEY
);
