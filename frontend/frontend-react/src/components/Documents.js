import React from 'react';
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import DriveIcon from '../static/images/docs.png'

export default function Document(props) {
    const docs = props.documents; // Use const to declare docs

    // Ensure JSX is wrapped in a single parent element, such as a div
    return (
        <div>
            <FormGroup >
            {docs.length !== 0 ? (
                docs.slice(0, 10).map((doc) => (
                    <div>
                        <FormControlLabel control={<Checkbox />} label={doc.name} />
                        <a target="_blank" href={doc.webViewLink}><img style= {{height:'20px', width:'20px'}}src={DriveIcon}/></a>
                    </div>
                    
                ))
            ) : (
                <h1>No documents found</h1> // Handle case where there are no documents
            )}
            </FormGroup>
        </div>
    );
}
