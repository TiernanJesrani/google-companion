import React, { useState } from 'react';
import { FormGroup, FormControlLabel, Checkbox, Button } from '@mui/material';
import DriveIcon from '../static/images/docs.png'; // Assuming you're using MUI icons

export default function Document(props) {
    const [selectedDocs, setSelectedDocs] = useState([]); // State to keep track of selected documents

    const docs = props.documents; // Use const to declare docs

    // Function to handle checkbox changes
    const handleCheckboxChange = (docId) => {
        setSelectedDocs(prevSelectedDocs =>
            prevSelectedDocs.includes(docId)
                ? prevSelectedDocs.filter(id => id !== docId) // Remove id if already selected
                : [...prevSelectedDocs, docId] // Add id if not selected
        );
    };

    // Function to handle form submission
    const handleSubmit = () => {
        // Use fetch to send data to your endpoint
        console.log(selectedDocs)
        fetch('http://127.0.0.1:5000/temu/add-doc', {
        method: 'POST', // Use POST method
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            documentIds: selectedDocs
        })
    })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            // Handle success here (e.g., showing a success message)
        })
        .catch((error) => {
            console.error('Error:', error);
            // Handle errors here (e.g., showing an error message)
        });
    };

    return (
        <div>
            <FormGroup>
                {docs.length !== 0 ? (
                    docs.slice(0, 10).map((doc) => (
                        <div key={doc.id}>
                            <FormControlLabel
                                control={
                                    <Checkbox
                                        checked={selectedDocs.includes(doc.id)}
                                        onChange={() => handleCheckboxChange(doc.id)}
                                    />
                                }
                                label={doc.name}
                            />
                            <a target="_blank" rel="noopener noreferrer" href={doc.webViewLink}>
                                <img style={{ height: '20px', width: '20px' }} src={DriveIcon} alt="Open Document"/>
                            </a>
                        </div>
                    ))
                ) : (
                    <h1>No documents found</h1>
                )}
            </FormGroup>
            <Button variant="contained" onClick={handleSubmit}>
                Submit
            </Button>
        </div>
    );
}
