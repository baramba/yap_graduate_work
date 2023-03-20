import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import {
    Accordion,
    AccordionSummary,
    AccordionDetails,
    Typography,
    Divider,
} from '@mui/material';


export default function TechInfo({ data }) {
    return (
        <>
            <Accordion>
                <AccordionSummary
                    expandIcon={<ExpandMoreIcon />}
                    aria-controls="panel1a-content"
                    id="panel1a-header"
                >
                    <Typography variant="subtitle1">Техническая информация</Typography>
                </AccordionSummary>
                <AccordionDetails>
                    <Typography variant="body1" component="pre">
                        {JSON.stringify(data, null, 2)}
                    </Typography>
                </AccordionDetails>
            </Accordion>
        </>
    )
}