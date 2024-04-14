import React, { useEffect } from 'react';
import { Card, CardContent, Typography, Box, Divider, formHelperTextClasses } from '@mui/material';
import ButtonGroup from '@mui/material/ButtonGroup';
import Button from '@mui/material/Button';
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { useState } from 'react';

function MeetingCard(props) {
  const { show_meetings } = props;
  const space_name = props.name
  const [summaries, setSummaries] = useState([])
  const [item, setItem] = useState("")
  const [items, setItems] = useState(Array(10))

  function summarize(name, id, index) {
    fetch(`http://127.0.0.1:5000/get-summary/${name}/${id}`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to load data');
        }
        let text = response.json()
        setSummaries([...[name,text]])
        return text
      })
      .then(data => {

        console.log(data[0])
        let temp_items = items
        temp_items[index] = data[0]
        setItems(temp_items)
        
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
      
    {show_meetings.map((meeting, index) => {
      return (
        <Accordion>
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          aria-controls="panel1-content"
          id="panel1-header"
        >
          <Typography>
            <strong>{meeting.summary}</strong> with <strong>{meeting.organizer.email}</strong>
            <ButtonGroup variant="outlined" aria-label="Loading button group" sx={{height: '75%', marginLeft: "100px", alignContent: 'center'}}>
                <Button onClick={() => summarize(space_name, meeting.conferenceData.conferenceId, index)}>Summarize</Button>
             </ButtonGroup>
            </Typography>
            
        </AccordionSummary>
        <AccordionDetails>
          <Typography>

            <strong>Summary:</strong> {items[index]}

          </Typography>
        </AccordionDetails>
      </Accordion>
    )
    })}</Box>
  );
}
export default MeetingCard;
