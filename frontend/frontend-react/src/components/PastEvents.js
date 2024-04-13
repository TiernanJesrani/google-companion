import React from 'react';
import { Card, CardContent, Typography, Box, Divider } from '@mui/material';
import ButtonGroup from '@mui/material/ButtonGroup';
import Button from '@mui/material/Button';
import LoadingButton from '@mui/lab/LoadingButton';
import SaveIcon from '@mui/icons-material/Save';
import googlemeet from '../static/images/google-meet.png'
function MeetingCard() {
  return (
    <Card sx={{ display: 'flex', alignItems: 'center' }}> 
    <img style={{height:'50px'}}src={googlemeet}/>
      <Box sx={{ display: 'flex', flexDirection: 'row', flex: 1 }}> 
        <CardContent sx={{ flex: '1 0 auto' }}>
            
          <Typography component="div" variant="h5">
            Meeting Name
          </Typography>
          <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
            <Typography variant="subtitle1" color="text.secondary" component="div">
              Duration - Attendees (cut off at 4)
            </Typography>
          </Box>
        </CardContent>
        <ButtonGroup variant="outlined" aria-label="Loading button group" sx={{height: '75%', marginRight: "150px", marginTop: '30px', alignContent: 'center'}}>
                <Button>Summarize</Button>
                <LoadingButton>Generate Tasks</LoadingButton>
                <LoadingButton loading loadingPosition="start" startIcon={<SaveIcon />}>
                    Save
                </LoadingButton>
            </ButtonGroup>
      </Box>
    </Card>
  );
}

export default MeetingCard;
