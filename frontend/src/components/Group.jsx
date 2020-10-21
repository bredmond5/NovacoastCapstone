import React, { useEffect, useState, useContext } from 'react'
import { Link, useHistory } from 'react-router-dom'
import { DateTime } from 'luxon'

import { StyledLink } from 'baseui/link'
import { ButtonGroup } from 'baseui/button-group'
import { Button, KIND as BUTTONKIND, SIZE } from 'baseui/button'
import { Select } from 'baseui/select'
import {
    StyledRoot,
    StyledTable,
    StyledTableHead,
    StyledTableBody,
    StyledTableHeadRow,
    StyledTableHeadCell,
    StyledTableBodyRow,
    StyledTableBodyCell,
} from 'baseui/table-semantic'
import { Tag, KIND as TAGKIND, VARIANT as TAGVARIANT } from 'baseui/tag'
import { Input } from 'baseui/input'
import { FormControl } from 'baseui/form-control'

import Data from '../Data.json'
import Context from '../Context'

// TODO
//  Send Email
//  Delete Group

function Group(props) {

    let history = useHistory()
    
    const context = useContext(Context)
    
    const [group, setGroup] = useState(null)
    const [emails, setEmails] = useState([])
    const [domains, setDomains] = useState([])

    const [emailChangeSuccess, setEmailChangeSuccess] = useState(null)

    const [addingNewDomain, setAddingNewDomain] = useState(false)
    const [newDomain, setNewDomain] = useState('')
    const [newDomainSuccess, setNewDomainSuccess] = useState(null)

    async function getData() {
        // let group = await context.backend.get('/groups/' + props.match.params.id)

        let group = Data.groups.find(g => g.id.toString() === props.match.params.id) || {
            id: props.match.params.id,
            name: 'Group ' + props.match.params.id,
            emails: 'jdoe@example.com;jappleseed@legends.com'
        }

        setGroup(group)
        setEmails(group.emails.split(';').map(e => ({ id: e, label: e })))

        // let domains = await context.backend.get('/domains?groupId=' + group.id)
        let domains = Data.domains.filter(domain => domain.groupId === group.id)
        setDomains(domains)
    }
    async function addDomain() {
        try {
            // await context.backend.post('/domains', {
            //     groupId: group.id,
            //     name: newDomain,
            // })
        } catch(e) {
            console.error(e)
            setNewDomainSuccess(false)
            setTimeout(() => setAddingNewDomain(false), 2000)
            return
        }

        setNewDomainSuccess(true)
        setTimeout(() => setAddingNewDomain(false), 1000)
        await getData()
    }
    async function deleteGroup() {
        try {
            // await context.backend.delete('/groups/' + group.id)
        } catch(e) {
            console.error(e)
            return
        }
        history.goBack()
    }
    async function setDomainStatus(domain, status) {
        try {
            // await context.backend.put('/domains/' + domain.id + '?status=' + status)
        } catch(e) {
            console.error(e)
            return
        }
        await getData()
    }

    useEffect(() => {
        getData()
    }, [props.match.params.id])

    useEffect(() => {
        if(group && emails.length !== group.emails.split(';').length) {
            try {
                context.backend.put('/groups/' + group.id)
            } catch(e) {
                console.error(e)
                setEmailChangeSuccess(false)
                setTimeout(() => setEmailChangeSuccess(null), 2000)
                // getData()
                return
            }
            setEmailChangeSuccess(true)
            setTimeout(() => setEmailChangeSuccess(null), 1000)
            // getData()
        }
    }, [emails])

    return(
        <div className='details group'>
            {group ?
                <>
                    {/* <Breadcrumbs className='breadcrumbs'>
                        <span>{group.name}</span>
                    </Breadcrumbs> */}
                    <h1>{group.name || 'Group ' + group.id}</h1>
                    <ButtonGroup>
                        <Button>Send Email</Button>
                        <Button onClick={deleteGroup}>Delete Group</Button>
                    </ButtonGroup>
                    <h3>Emails</h3>
                    <FormControl caption={emailChangeSuccess === true ? 'Saved' : (emailChangeSuccess === false ? 'Failed' : '')}>
                        <Select
                            key={emailChangeSuccess !== false}
                            creatable
                            value={emails}
                            multi
                            placeholder='Add an email'
                            openOnClick={false}
                            onChange={({ value }) => setEmails(value)}
                            positive={emailChangeSuccess === true}
                            error={emailChangeSuccess === false}
                            backspaceRemoves={false}
                            clearable={false}
                            closeOnSelect={false}
                            deleteRemoves={false}
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
                    <h3>Domains</h3>
                    <StyledRoot>
                        <StyledTable className='domains-table'>
                            <StyledTableHead>
                                <StyledTableHeadRow>
                                    <StyledTableHeadCell>Status</StyledTableHeadCell>
                                    <StyledTableHeadCell>Domain</StyledTableHeadCell>
                                    <StyledTableHeadCell>Hits</StyledTableHeadCell>
                                    <StyledTableHeadCell>Last Emailed</StyledTableHeadCell>
                                    <StyledTableHeadCell>Date Created</StyledTableHeadCell>
                                </StyledTableHeadRow>
                            </StyledTableHead>
                            <StyledTableBody>
                                {domains.map(domain => {
                                    let tag
                                    if(domain.active) {
                                        tag = <Tag onClick={() => setDomainStatus(domain, true)} closeable={false} kind={TAGKIND.positive}>Active</Tag>
                                    } else {
                                        tag = <Tag onClick={() => setDomainStatus(domain, false)} closeable={false} kind={TAGKIND.negative}>Inactive</Tag>
                                    }
                                    let hits = Data.lookalikes.filter(lookalike => lookalike.domainId === domain.id)
                                    return <StyledTableBodyRow key={domain.id}>
                                        <StyledTableBodyCell>{tag}</StyledTableBodyCell>
                                        <StyledTableBodyCell>
                                            <Link to={{
                                                pathname: '/domain/' + domain.id,
                                                state: { domain, group }
                                            }}>
                                                <StyledLink>{domain.name}</StyledLink>
                                            </Link>
                                        </StyledTableBodyCell>
                                        <StyledTableBodyCell>
                                            <Tag 
                                                closeable={false} 
                                                variant={TAGVARIANT.solid}
                                                overrides={{
                                                    Root: {
                                                        style: () => ({
                                                            backgroundColor: 'rgb(' + Math.min(hits.length*16, 256) + ', 0, 0)'
                                                        })
                                                    }
                                                }}
                                            >
                                                {hits.length}
                                            </Tag>
                                        </StyledTableBodyCell>
                                        <StyledTableBodyCell>{domain.lastEmailed ? DateTime.fromISO(domain.lastEmailed, {setZone: true}).toFormat('y, MMM dd, hh:mm a') : '-'}</StyledTableBodyCell>
                                        <StyledTableBodyCell>{domain.createdAt ? DateTime.fromISO(domain.createdAt, {setZone: true}).toFormat('y, MMM dd, hh:mm a') : '-'}</StyledTableBodyCell>
                                    </StyledTableBodyRow>
                                })}
                                {addingNewDomain ?
                                    <StyledTableBodyRow className='add-new-domain-row adding-form'>
                                        <StyledTableBodyCell colSpan='5' style={{ padding: '16px' }}>
                                            <FormControl style={{ margin: 0 }}>
                                                <Input
                                                    type='text'
                                                    autoFocus
                                                    value={newDomain}
                                                    onChange={e => setNewDomain(e.target.value)}
                                                    // onBlur={() => setAddingNewDomain(false)}
                                                    placeholder='Add New Domain'
                                                    clearOnEscape
                                                    endEnhancer={() => 
                                                        <Button size={SIZE.mini} kind={BUTTONKIND.primary} onClick={() => addDomain()} style={{ whiteSpace: 'nowrap' }}>
                                                            Add Domain
                                                        </Button>
                                                    }
                                                    error={newDomainSuccess === false}
                                                    positive={newDomainSuccess === true}
                                                />
                                            </FormControl>
                                        </StyledTableBodyCell>
                                    </StyledTableBodyRow>
                                :
                                    <StyledTableBodyRow className='add-new-domain-row' onClick={() => setAddingNewDomain(true)}>
                                        <StyledTableBodyCell colSpan='5'><em>+ Add New Domain</em></StyledTableBodyCell>
                                    </StyledTableBodyRow>
                                }
                            </StyledTableBody>
                        </StyledTable>
                    </StyledRoot>
                </>
            : null }
        </div>
    )

}

export default Group