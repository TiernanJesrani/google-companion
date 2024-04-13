import logo from './logo.svg';
import './App.css';
import Grid from '@mui/material/Grid';
import Item from '@mui/material/Paper';
import { Box } from '@mui/material';


// 
import { useState } from 'react';

// components
import Space from './components/Space';
import CreateSpace from './components/CreateSpace'
// images (replace)
import mhacks from './static/images/mhacks.png'
import campus from './static/images/campus.jpeg'

function App() {
  const [showCreate, setShowCreate] = useState(false)
  const [gridItems, setGridItems] = useState(
    [
      {
        "name": "Google/MHacks Hackthon",
        "date_created": '4-12-24',
        "button_title": 'Enter',
        'tags': ['school', 'e/acc', 'hackathons'],
        'image': mhacks
      },
      {
        "name": "Dr. Google Research Lab",
        "date_created": '3-4-24',
        "button_title": 'Enter',
        'tags': ['school', 'research'],
        'image': campus
      },
    ]
  )
  return (
    <div className="App">
      <header className="App-header">
        {showCreate && 
          <CreateSpace/>
        }
      <Grid container spacing={8}>
          {gridItems.map((item) => ( 
            <Grid item xs={6}>
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
      </header>
      
    </div>
  );
}

export default App;
