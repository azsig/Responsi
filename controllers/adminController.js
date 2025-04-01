exports.showLogin = (req, res) => {
  res.render('login');
};

exports.handleLogin = (req, res) => {
  const { username, password } = req.body;
  if (username === 'admin' && password === 'admin') {
    req.session.isAdmin = true;
    res.redirect('/admin/dashboard');
  } else {
    res.send('Invalid credentials');
  }
};

exports.showAdminDashboard = (req, res) => {
  if (!req.session.isAdmin) {
    return res.redirect('/admin/login');
  }
  res.render('adminDashboard');
};

exports.handleEmergency = (req, res) => {
  res.send('Emergency button clicked!');
};