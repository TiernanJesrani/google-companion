import React from 'react';
import { Card, CardContent, Typography, Box, Divider } from '@mui/material';
import ButtonGroup from '@mui/material/ButtonGroup';
import Button from '@mui/material/Button';
import LoadingButton from '@mui/lab/LoadingButton';
import SaveIcon from '@mui/icons-material/Save';
import googlemeet from '../static/images/google-meet.png'
function MeetingCard(props) {
  const { show_meetings } = props;
  console.log(show_meetings.length)

  function summarize(name, id) {
    console.log(name, id)
    fetch(`http://127.0.0.1:5000/get-summary/${name}/${id}`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to load data');
        }
        console.log(response)
        return response.json();
      })
      .then(data => {
        console.log(data)
      })
      .catch(error => {
        console.error("Error fetching data", error);
      });
  }

  if (show_meetings.length === 0 || show_meetings[0].length === 0) {
    console.log("none")
    return <h1>Select meetings to add!</h1>
  }
  return (
    <Box>
      
    {show_meetings.map((meeting) => {
      return (
      <Card sx={{ display: 'flex', alignItems: 'center', paddingTop: '15px'}}> 
    <img style={{height:'50px'}}src={googlemeet}/>
      <Box sx={{ display: 'flex', flexDirection: 'row', flex: 1 }}> 
        <CardContent sx={{ flex: '1 0 auto' }}>
            
          <Typography component="div" variant="h5">
            {console.log("meeting:" + JSON.stringify(meeting))}
            {meeting[0].summary}
          </Typography>
          <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
            <Typography variant="subtitle1" color="text.secondary" component="div">
              {meeting[0].attendees.map((attendee) => {
                if (attendee.organizer === true) {
                  return attendee.email 
                }
              })}
            </Typography>
          </Box>
        </CardContent>
        <ButtonGroup variant="outlined" aria-label="Loading button group" sx={{height: '75%', marginRight: "150px", marginTop: '30px', alignContent: 'center'}}>
                <Button onClick={() => summarize('space', meeting[0].conferenceData.conferenceId)}>Summarize</Button>
                {console.log(meeting)}
                <LoadingButton>Generate Tasks</LoadingButton>
                <LoadingButton loading loadingPosition="start" startIcon={<SaveIcon />}>
                    Save
                </LoadingButton>
            </ButtonGroup>
      </Box>
    </Card>)
    })}</Box>
  );
}
export default MeetingCard;
