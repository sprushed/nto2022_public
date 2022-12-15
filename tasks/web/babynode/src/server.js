const express = require('express');
const hbs  = require('express-handlebars');
const cookieSession = require('cookie-session');
const cookieParser = require('cookie-parser');
const bodyParser = require('body-parser');
const mysql = require('mysql');

const HOST = '0.0.0.0';
const PORT = process.env.PORT ?? '8337';
const SECRET_KEY = process.env.SECRET_KEY || 's3cret';

const app = express();

app.engine('handlebars', hbs.engine());
app.set('view engine', 'handlebars');

app.use(cookieParser());
app.use(cookieSession({
    name: 'session',
    keys: [SECRET_KEY],
}));

app.use(bodyParser.urlencoded({
    extended: true
}));

const ensureAuth = (req, res, next) => {
    if (!req.session?.username) {
      return res.redirect('/login');
    }
    next();
};

app.get('/', (req, res) => {
    res.render('index');
});

app.get('/profile', ensureAuth, (req, res) => {
    if (req.session.is_admin)
        res.render('profile', {
            username: req.session.username,
            flag: process.env.FLAG || 'NTO{flaghere}'
        });
    else
        res.render('profile', {
            username: req.session.username
        });
});

app.post('/logout', ensureAuth, (req, res) => {
    req.session = null;
    res.clearCookie('connect.sid');
    res.redirect('/login');
});

app.get('/login', (req, res) => res.render('login'));
app.post('/login', (req, res) => {
    const { username, password } = req.body;

    const client = mysql.createConnection({
                        host: process.env.DB_HOST || 'localhost',
                        user: process.env.DB_USER || 'moderator',
                        password: process.env.DB_PASSWORD || 'moderator',
                        database: process.env.DATABASE || 'nto',
                        insecureAuth: true
                    });
    client.connect();

    client.query('SELECT * FROM users WHERE username = ? AND password = ? ORDER BY id', [username, password], (err, out) => {
        client.destroy();
        console.log(out);
        if(err) {
            res.render('login', {error: `Unknown error: ${err}`});
        } else if(out.length) {
            req.session.username = out[0]['username'];
            req.session.is_admin = out[0]['is_admin'];
            res.redirect('/profile');
        } else {
            res.render('login', {error: 'Invalid username or password'});
        }
    });
});

app.get('/register', (req, res) => res.render('register'));
app.post('/register', async (req, res) => {
    const { username, password } = req.body;

    const client = mysql.createConnection({
        host: process.env.DB_HOST || 'localhost',
        user: process.env.DB_USER || 'moderator',
        password: process.env.DB_PASSWORD || 'moderator',
        database: process.env.DATABASE || 'nto',
        insecureAuth: true
    });
    client.connect();

    client.query('SELECT * FROM users WHERE username = ? AND password = ? ORDER BY id', [username, password], (err, out) => {
        if(err) {
            client.destroy();
            res.render('register', {error: `Unknown error: ${err}`});
        } else if(out.length) {
            client.destroy();
            res.render('register', {error: 'Failed to register user'});
        } else {
            client.query(
                'INSERT INTO `users` (username, password, is_admin) VALUES (?,?,FALSE);',
                [username, password],
                (err, out) => {
                    client.destroy();
                    if(err)
                        res.render('register', {error: `Unknown error: ${err}`});
                    else
                    res.redirect('/login');
                });
        }
    });
});

app.listen(PORT, HOST, () => console.log(`Listening on ${HOST}:${PORT}`));
