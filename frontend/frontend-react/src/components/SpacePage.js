import React from 'react';
import { Box, Tab, Tabs, Typography, Breadcrumbs, Link } from '@mui/material';
import { json, useLocation, useParams } from 'react-router-dom';
import SpeedDial from '@mui/material/SpeedDial';
import SpeedDialIcon from '@mui/material/SpeedDialIcon';
import SpeedDialAction from '@mui/material/SpeedDialAction';
import Button from '@mui/material/Button';
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import Calendar from './Calendar';
import googlemeet from '../static/images/google-meet.png'
import docs from '../static/images/docs.png'
import MeetingCard from './PastEvents'
import Chatbot from 'react-chatbot-kit'
import 'react-chatbot-kit/build/main.css'
import config from './config.js';
import MessageParser from '../components/MessageParser.js';
import ActionProvider from './ActionProvider.js';

function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          <Typography>{children}</Typography>
        </Box>
      )}
    </div>
  );
}

function a11yProps(index) {
  return {
    id: `simple-tab-${index}`,
    'aria-controls': `simple-tabpanel-${index}`,
  };
}

export default function App() {
  const [value, setValue] = React.useState(0);
  const [showAdd, setShowAdd] = React.useState(false)
  const route = useLocation()
  const [meetings, setMeetings] = React.useState([])
  const [isLoading, setIsLoading] = React.useState(false);
  const [error, setError] = React.useState(null);
  const [chosenMeetings, setChosenMeetings] = React.useState([]);
  const [checkedMeetings, setCheckedMeetings] = React.useState([]);
  const [docs, setDocs] = React.useState([])

  const actions = [
    { 
        icon: <img src={googlemeet} className="google-meet-icon" style={{ width: '24px', height: '24px' }} alt="Google Meet" />, 
        name: 'Google Meet', 
        onClick: () => prepAdd(true) 
    },
    { 
      icon: <img src={docs} className="docs-icon" style={{ width: '24px', height: '24px' }} alt="Documents" />, 
      name: 'Documents', 
      onClick: () => prepAdd(true) 
    } 
  ];
  const handleChange = (event, newValue) => {
    setValue(newValue);
  };
  const handleClose = () => {
    setShowAdd(false);
  };
  const prepAdd = (setShow) => {
    setShowAdd(setShow)
  }
  const handleCheckboxChange = (meeting, isChecked) => {
    if (isChecked) {
      // Add the meeting to the array if it's checked
      setCheckedMeetings(prevMeetings => [...prevMeetings, meeting]);
    } else {
      // Remove the meeting from the array if it's unchecked
      setCheckedMeetings(prevMeetings => prevMeetings.filter(m => m.id !== meeting.id));
    }
  };

  function choseMeetings() {
    setChosenMeetings(checkedMeetings)

    console.log(chosenMeetings)
  }

  React.useEffect(() => {
    setIsLoading(true);
    console.log("fetching")
    fetch('http://127.0.0.1:5000/add-to-space')
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to load data');
        }
        return response.json();
      })
      .then(data => {
        console.log("fetching meeting: ")
        console.log(typeof meetings)
        console.log(data.meetings)
        setMeetings((data.meetings));
        setIsLoading(false);
      })
      .catch(error => {
        console.error("Error fetching data", error);
        setError(error.toString());
        setIsLoading(false);
      });


    fetch('http://127.0.0.1:5000/add-docs-to-space')
    .then(response => {
      if (!response.ok) {
        throw new Error('Failed to load data');
      }
      return response.json();
    })
    .then(data => {
      console.log("docs" + JSON.stringify(data[15]))
      setDocs(data)
    })
    .catch(error => {
      console.error("Error fetching data", error);
      setError(error.toString());
      setIsLoading(false);
    });
  }, []);

  function getData(param) {
    const savedItems = JSON.parse(localStorage.getItem('gridItems'));

    const item = savedItems.find(item => route.pathname.split('/')[2] === item.route);
    return item[param]
  }

  return (
    <Box sx={{ flexGrow: 1, minHeight: '100vh', bgcolor: '#4285F4', p: 2 }}>
      <Box sx={{ 
          borderRadius: 4, 
          bgcolor: 'background.paper', 
          boxShadow: 1, 
          p: 2, 
          minHeight: '90vh', 
          margin: 'auto', 
          maxWidth: 'md' 
        }}>

        <Breadcrumbs aria-label="breadcrumb">
        <Link underline="hover" color="inherit" href="/home">
            Home
        </Link>
        <Link
            color="inherit"
        >
            <div>{getData("name")}</div>
        </Link>       
        <Calendar
            date={getData("date_created")}
       />
       
        </Breadcrumbs>
        <Tabs value={value} onChange={handleChange} aria-label="basic tabs example" centered>
          <Tab label="Space Home" {...a11yProps(0)} />
          <Tab label="Past Events" {...a11yProps(1)} />
          <Tab label="Documents" {...a11yProps(2)} />
        </Tabs>
        <TabPanel value={value} index={0} >
          <div style={{ height: '100%', // Ensures the div fills the height of its container
            width: '100%', // Ensures the div fills the width of its container
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            padding: '24px' }} >
      
        <Chatbot
          config={config}
          messageParser={MessageParser}
          actionProvider={ActionProvider}
          style={{
            width: '100%', // Ensures Chatbot fills the width of its container
            height: '100%' // Ensures Chatbot fills the height of its container
          }}
      /></div>
        </TabPanel>
        <TabPanel value={value} index={1}>
          <MeetingCard 
            show_meetings={chosenMeetings}
            name={route.pathname.split('/')[2]}
          />
        </TabPanel>
        <TabPanel value={value} index={2}>
          Documents
        </TabPanel>
        
      </Box>
        <SpeedDial
            ariaLabel="SpeedDial basic example"
            sx={{ position: 'absolute', bottom: 16, right: 16 }}
            icon={<SpeedDialIcon />}
            >
            {actions.map((action) => (
                <SpeedDialAction
                key={action.name}
                icon={action.icon}
                tooltipTitle={action.name}
                onClick={action.onClick}
                />
            ))}
        </SpeedDial>
        {showAdd &&  <React.Fragment>
      <Dialog
        open={showAdd}
        onClose={handleClose}
        PaperProps={{
          component: 'form',
          onSubmit: (event) => {
            event.preventDefault();
            const formData = new FormData(event.currentTarget);
            const formJson = Object.fromEntries(formData.entries());
            const name = formJson.name;
            console.log(`Created Space named ${name}`)
            handleClose(name);
          },
        }}
      >
        <DialogTitle>Add meeting</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Select meetings to add to {getData("name")}
          </DialogContentText>
          <FormGroup>
          {meetings.length > 0 ? (
        <ul>
          {console.log(meetings.length)}
          {meetings.map((meeting, index) => (
            <FormControlLabel
              control={
              <Checkbox 
                checked={checkedMeetings.some(m => m.id === meeting.id)}
                onChange={(e) => handleCheckboxChange(meeting, e.target.checked)}
              />
            }
              key={index} 
              label={meeting.summary + ' -- ADD DATE'}  />
          
          ))}
        </ul>
      ) : (
        <p>No meetings found.</p>
      )}
        </FormGroup>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancel</Button>
          <Button type="submit" onClick={choseMeetings}>Create</Button>
        </DialogActions>
      </Dialog>
    </React.Fragment>}
    </Box>
  );
}
