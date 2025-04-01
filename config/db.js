const { Pool } = require('pg');

const pool = new Pool({
  user: 'azsig',
  host: 'localhost',
  database: 'responsi',
  password: '112141linux',
  port: 5432,
});

module.exports = pool;