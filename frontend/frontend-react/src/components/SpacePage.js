import React from 'react';
import { Box, Tab, Tabs, Typography, Breadcrumbs, Link } from '@mui/material';
import { useLocation, useParams } from 'react-router-dom';
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
import PastEvents from './PastEvents'

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
  const actions = [
    { 
        icon: <img src={googlemeet} className="google-meet-icon" style={{ width: '24px', height: '24px' }} alt="Google Meet" />, 
        name: 'Google Meet', 
        onClick: () => setShowAdd(true) 
    },
    { 
      icon: <img src={docs} className="google-meet-icon" style={{ width: '24px', height: '24px' }} alt="Doocuments" />, 
      name: 'Documents', 
      onClick: () => setShowAdd(true) 
    } 
  ];
  const handleChange = (event, newValue) => {
    setValue(newValue);
  };
  const handleClose = () => {
    setShowAdd(false);
  };

  function getData(param) {
    const savedItems = JSON.parse(localStorage.getItem('gridItems'));
    console.log(route)
    console.log("route: " + savedItems[0].route)
    const item = savedItems.find(item => route.pathname.split('/')[2] === item.route);
    
    console.log(item)
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
          <Tab label="Upcoming" {...a11yProps(0)} />
          <Tab label="Past Events" {...a11yProps(1)} />
        </Tabs>
        <TabPanel value={value} index={0}>
          Content for Tab One
        </TabPanel>
        <TabPanel value={value} index={1}>
          <PastEvents />
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
            <FormControlLabel control={<Checkbox />} label="Label" />
            <FormControlLabel control={<Checkbox />} label="Label" />
            <FormControlLabel control={<Checkbox />} label="Label" />
            <FormControlLabel control={<Checkbox />} label="Label" />
        </FormGroup>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancel</Button>
          <Button type="submit">Create</Button>
        </DialogActions>
      </Dialog>
    </React.Fragment>}
    </Box>
  );
}
