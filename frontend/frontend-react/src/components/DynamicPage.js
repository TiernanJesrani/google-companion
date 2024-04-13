import React from 'react';
import { Box, Tab, Tabs, Typography, Breadcrumbs, Link } from '@mui/material';
import { useLocation, useParams } from 'react-router-dom';
import SpeedDial from '@mui/material/SpeedDial';
import SpeedDialIcon from '@mui/material/SpeedDialIcon';
import SpeedDialAction from '@mui/material/SpeedDialAction';
import FileCopyIcon from '@mui/icons-material/FileCopyOutlined';
import SaveIcon from '@mui/icons-material/Save';
import PrintIcon from '@mui/icons-material/Print';
import ShareIcon from '@mui/icons-material/Share';
import { DemoContainer } from '@mui/x-date-pickers/internals/demo';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import Calendar from './Calendar';

const actions = [
    { icon: <FileCopyIcon />, name: 'Copy' },
    { icon: <SaveIcon />, name: 'Save' },
    { icon: <PrintIcon />, name: 'Print' },
    { icon: <ShareIcon />, name: 'Share' },
  ];

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
  const [gridItem, setGridItem] = React.useState({})
  const route = useLocation()
  const handleChange = (event, newValue) => {
    setValue(newValue);
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
    <Box sx={{ flexGrow: 1, minHeight: '100vh', bgcolor: 'background.default', p: 4 }}>
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
        {/* <Typography color="text.primary"><div>{getData("date_created")}</div></Typography> */}
       {
        <Calendar
            date={getData("date_created")}
       />
       }
        </Breadcrumbs>
        <Tabs value={value} onChange={handleChange} aria-label="basic tabs example" centered>
          <Tab label="Upcoming" {...a11yProps(0)} />
          <Tab label="Past Events" {...a11yProps(1)} />
        </Tabs>
        <TabPanel value={value} index={0}>
          Content for Tab One
        </TabPanel>
        <TabPanel value={value} index={1}>
          Content for Tab Two
        </TabPanel>
        <TabPanel value={value} index={2}>
          Content for Tab Three
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
                />
            ))}
        </SpeedDial>
    </Box>
  );
}
