import React, { useState, useEffect, useContext } from 'react'
import { useHistory } from 'react-router-dom'

import { Input } from 'baseui/input'
import { Select } from 'baseui/select'
import { Button, SIZE } from 'baseui/button'
import { FormControl } from 'baseui/form-control'
import { FileUploader } from 'baseui/file-uploader'

import Context from '../Context'

function AddGroup(props) {

    console.log(props)

    let history = useHistory()
    const context = useContext(Context)

    const [name, setName] = useState('')
    const [emails, setEmails] = useState([])

    const [adding, setAdding] = useState(false)
    const [success, setSuccess] = useState(null)

    const [errorMessage, setErrorMessage] = useState('')

    useEffect(() => {
        if(adding) {
            if(success === true) {
                setSuccess(null)
                setAdding(false)
                setName('')
                setEmails([])
            } else if(success === false) {
                setSuccess(null)
                setAdding(false)
            } else {
                addGroup()
            }
        }
    }, [adding])

    async function addGroup() {
        let newGroup
        try {
            // newGroup = await context.backend.post('/groups', {
            //     name,
            //     emails: emails.join(';')
            // })
        } catch(e) {
            console.error(e)
            setTimeout(() => setAdding(false), 2000)
            setSuccess(false)
            return
        }
        setTimeout(() => setAdding(false), 1000)
        setSuccess(true)
    }

    let buttonString = 'Add Group'
    if(success === true) {
        buttonString = 'Added Group!'
    } else if(success === false) {
        buttonString = 'Failed.'
    } else if(adding) {
        buttonString = 'Adding...'
    }

    return(
        <div className='add-group'>
            <h1>Add Group</h1>
            <FormControl label='Name'>
                <Input
                    value={name}
                    onChange={e => setName(e.target.value)}
                    placeholder='Enter a name for this group'
                    type='text'
                    autoFocus
                />
            </FormControl>
            <FormControl label='Emails'>
                <Select
                    creatable
                    value={emails}
                    multi
                    placeholder='Add an email'
                    openOnClick={false}
                    onChange={({ value }) => setEmails(value)}
                    overrides={{
                        IconsContainer: {
                            style: () => ({
                                display: 'none'
                            })
                        }, DropdownContainer: {
                            style: () => ({
                                display: 'none'
                            })
                        }
                    }}
                />
            </FormControl>
            <FormControl label='Domains' caption='optional'>
                <FileUploader 
                    accept={['.txt', '.csv']}
                    errorMessage={errorMessage}
                />
            </FormControl>
            <br/>
            <Button
                onClick={() => setAdding(true)}
                size={SIZE.large}
                isLoading={adding}
                disabled={adding || !name || emails.length === 0}
            >
                {buttonString}
            </Button>
        </div>
    )

}

export default AddGroup