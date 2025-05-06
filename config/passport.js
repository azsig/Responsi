const LocalStrategy = require('passport-local').Strategy;
const bcrypt = require('bcryptjs');
const db = require('./db'); // Import konfigurasi database

module.exports = function (passport) {
    // Konfigurasi strategi login menggunakan username dan password
    passport.use(
        new LocalStrategy(async (username, password, done) => {
            try {
                // Cari user berdasarkan username
                const result = await db.query('SELECT * FROM users WHERE username = $1', [username]);
                const user = result.rows[0];

                if (!user) {
                    return done(null, false, { message: 'Incorrect username' });
                }

                // Bandingkan password yang diinput dengan password yang di-hash di database
                const isMatch = await bcrypt.compare(password, user.password);
                if (!isMatch) {
                    return done(null, false, { message: 'Incorrect password' });
                }

                // Jika username dan password cocok, kembalikan user
                return done(null, user);
            } catch (error) {
                console.error('Error during authentication:', error);
                return done(error);
            }
        })
    );

    // Serialisasi user untuk disimpan di session
    passport.serializeUser((user, done) => {
        done(null, user.id);
    });

    // Deserialisasi user berdasarkan ID dari session
    passport.deserializeUser(async (id, done) => {
        try {
            const result = await db.query('SELECT * FROM users WHERE id = $1', [id]);
            const user = result.rows[0];
            done(null, user);
        } catch (error) {
            console.error('Error during deserialization:', error);
            done(error, null);
        }
    });
};