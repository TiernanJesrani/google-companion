import logo from './logo.svg';
import './App.css';
import * as React from 'react';
import Grid from '@mui/material/Grid';
import { Box } from '@mui/material';
import { useState, useEffect } from 'react';
import Space from './components/SpaceCard';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import { googleLogout, useGoogleLogin } from '@react-oauth/google';
import axios from 'axios';
import mhacks from './static/images/mhacks.png'
import campus from './static/images/campus.jpeg'

function Home() {
  const [showCreate, setShowCreate] = useState(false)
  const [nameToCreate, setNameToCreate] = useState("")
  const [loggedIn, setLoggedIn] = useState(false)
  const [user, setUser ] = useState([]);
  const [profile, setProfile ] = useState([]);
  const login = useGoogleLogin({
    onSuccess: (codeResponse) => {
      setUser(codeResponse)
    },
    onError: (error) => console.log('Login Failed:', error)
});
  const handleClickOpen = () => {
    setShowCreate(true);
  };
  const [gridItems, setGridItems] = useState(() => {
    // Retrieve the items from local storage; if none exist, use the default array
    const savedItems = localStorage.getItem('gridItems');
    return savedItems ? JSON.parse(savedItems) : [
      {
        "name": "Google/MHacks Hackthon",
        "route": convertToRoute("Google/MHacks Hackthon"),
        "date_created": 'April 12, 2024',
        "button_title": 'Enter',
        'tags': ['school', 'e/acc', 'hackathons'],
        'image': mhacks
      },
      {
        "name": "Dr. Google Research Lab",
        "route": convertToRoute("Dr. Google Research Lab"),
        "date_created": 'March 4, 2024',
        "button_title": 'Enter',
        'tags': ['school', 'research'],
        'image': campus
      },
    ];
  });
  useEffect(() => {
    if (user) {
      console.log(user.access_token)
      axios
          .get(`https://www.googleapis.com/oauth2/v1/userinfo?access_token=${user.access_token}`, {
              headers: {
                  Authorization: `Bearer ${user.access_token}`,
                  Accept: 'application/json'
              }
          })
          .then((res) => {
              setProfile(res.data);
              setLoggedIn(true)
          })
          .catch((err) => console.log(err));
    }
    // Store gridItems in local storage whenever they change
    localStorage.setItem('gridItems', JSON.stringify(gridItems));
  }, [gridItems], [user]);
  const logOut = () => {
    googleLogout();
    setProfile(null);
};

  function convertToRoute(str) {
    return str
      .trim() 
      .toLowerCase()
      .replace(/[^a-z0-9 ]/gi, '') 
      .replace(/\s+/g, '-') 
      .replace(/-+/g, '-'); 
  }

  const responseMessage = (response) => {
    setLoggedIn(true)
    console.log(response);
  };
  const errorMessage = (error) => {
      console.log(error);
  };


  const handleClose = (name) => {
    let date = new Date();
    let formatter = new Intl.DateTimeFormat('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
    console.log(`Created ${name} at ${formatter.format(date)}`); 
    setGridItems(gridItems => [...gridItems, 
      {
      "name": name,
      "route": convertToRoute(name),
      "date_created": formatter.format(date),
      "button_title": 'Enter',
      'tags': [],
      'image': mhacks
      }
    ])
    setShowCreate(false);
  };
  if (!loggedIn) {
    return (
      <div>
            <h2>React Google Login</h2>
            <br />
            <br />
            {profile ? (
                <div>
                    <img src={profile.picture} alt="user image" />
                    <h3>User Logged in</h3>
                    <p>Name: {profile.name}</p>
                    <p>Email Address: {profile.email}</p>
                    <br />
                    <br />
                    <button onClick={logOut}>Log out</button>
                </div>
            ) : (
                <button onClick={login}>Sign in with Google 🚀 </button>
            )}
        </div>
    );
  }
  return (
    
    <div className="App">
      <header className="App-header">
      <Grid container spacing={8} sx={{width:'80%'}}>
          {gridItems.map((item, index) => ( 
            <Grid item xs={6} key={index}>
            <Box display="flex" justifyContent="center" alignItems="center" height="100%">
                  <Space 
                    name={item.name}
                    date_created={"Created: " + item.date_created}
                    button_title={item.button_title}
                    tags={item.tags}
                    image={item.image}
                    setShowCreate={setShowCreate}
                  />
                </Box>
            </Grid>
          ))}
          <Grid item xs={6}>
            <Box display="flex" justifyContent="center" alignItems="center" height="100%">
            <Space 
                    name={"Add a new space!"}
                    date_created={"Create a world with Google"}
                    button_title={"Create new"}
                    tags={[]}
                    setShowCreate={setShowCreate}
                  />
                </Box>
            </Grid>
      </Grid>
      {showCreate &&  <React.Fragment>
      <Dialog
        open={showCreate}
        onClose={handleClose}
        PaperProps={{
          component: 'form',
          onSubmit: (event) => {
            event.preventDefault();
            const formData = new FormData(event.currentTarget);
            const formJson = Object.fromEntries(formData.entries());
            const name = formJson.name;
            console.log(`Created Space named ${name} `)
            handleClose(name);
          },
        }}
      >
        <DialogTitle>Create a space</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Create a new space with just a name!
          </DialogContentText>
          <TextField
            autoFocus
            required
            margin="dense"
            id="name"
            name="name"
            label="John Doe"
            type="text"
            fullWidth
            variant="standard"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancel</Button>
          <Button type="submit">Create</Button>
        </DialogActions>
      </Dialog>
    </React.Fragment>}
      </header>
      
    </div>
  );
}

export default Home;
