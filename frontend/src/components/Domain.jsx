import React, { useEffect, useState, useContext } from 'react'
import { Link, useHistory } from 'react-router-dom'
import { DateTime } from 'luxon'

import { Breadcrumbs } from 'baseui/breadcrumbs'
import { FormControl } from 'baseui/form-control'
import { Input, SIZE as INPUTSIZE } from 'baseui/input'
import { ButtonGroup, MODE } from 'baseui/button-group'
import { Button, KIND as BUTTONKIND } from 'baseui/button'
import { DatePicker } from 'baseui/datepicker'
import { TimePicker } from 'baseui/timepicker'
import { TimezonePicker } from 'baseui/timezonepicker'
import {
    StyledRoot,
    StyledTable,
    StyledTableHeadRow,
    StyledTableHeadCell,
    StyledTableBodyRow,
    StyledTableBodyCell,
    StyledTableHead,
    StyledTableBody,
} from 'baseui/table-semantic'
import {
    Modal,
    ModalHeader,
    ModalBody,
    ModalFooter,
    ModalButton,
    ROLE as MODALROLE,
    SIZE as MODALSIZE
} from 'baseui/modal'

import Context from '../Context'
import Data from '../Data.json'
import { Tag, KIND as TAGKIND, VARIANT,  } from 'baseui/tag'

function Domain(props) {

    let history = useHistory()
    const context = useContext(Context)

    const [domain, setDomain] = useState(null)
    const [group, setGroup] = useState(null)

    const [deleting, setDeleting] = useState(false)

    const [editing, setEditing] = useState()
    const [editingSuccess, setEditingSuccess] = useState(null)
    const [name, setName] = useState('')

    const [recurEditing, setRecurEditing] = useState(false)
    const [recur, setRecur] = useState('') // 'daily', 'weekly', 'monthly'
    const [recurRadio, setRecurRadio] = useState(null)
    const [recurDate, setRecurDate] = useState([])
    const [recurTime, setRecurTime] = useState(null)
    const [recurTz, setRecurTz] = useState(null)

    async function getDomain() {
        // let domain = await context.backend.get('/domains/' + props.match.params.id)
        let domain = Data.domains.find(d => d.id === parseInt(props.match.params.id))
        setDomain(domain)
        setName(domain.name)
        setRecur(domain.recur)
        switch(domain.recur) {
            case 'daily': setRecurRadio(0)
            break
            case 'weekly': setRecurRadio(1)
            break
            case 'monthly': setRecurRadio(2)
            break
            default: console.error('domain.recur retrieval error')
        }
        setRecurDate(DateTime.fromISO(domain.startAt).toJSDate())
        setRecurTime(DateTime.fromISO(domain.startAt).toJSDate())
        setRecurTz(domain.tz)
    }
    async function getGroup() {
        // let group = await context.backend.get('/groups/' + domain.groupId)
        let group = Data.groups.find(g => g.id === domain.groupId)
        setGroup(group)
    }

    async function changeName() {

        // return if unchanged
        if(domain.name === name) {
            setEditing(false)
            return
        }

        // backend call to change name
        try {
            // await context.backend.put('/domains/' + domain.id + '?name="' + name + '"')
        } catch (e) {
            console.error(e)
            setEditingSuccess(false)
            setTimeout(() => setEditing(false), 2000)
            return
        }

        // on success just change name locally, no need to get fresh object
        setEditingSuccess(true)
        domain.name = name

        // unmount input
        setTimeout(() => setEditing(false), 1000)

    }
    async function updateRecur() {

    }
    async function deleteDomain() {
        // delete domain

        history.replace('/group/' + group.id, { deletedDomain: domain })

    }

    useEffect(() => {
        getDomain()
    }, [props.match.params.id])

    useEffect(() => {
        if(domain)
            getGroup()
    }, [domain])

    useEffect(() => {
        console.log("Recurrence:", recur, recurDate[0], recurTime, recurTz)
    }, [recur])

    useEffect(() => {
        console.log("Recurrence TZ:", recurTz)
    }, [recurTz])

    function recurrenceInfo() {
        let startAt = DateTime.fromISO(domain?.startAt, { zone: recurTz })
        if(!startAt.isValid) { return <div/> }

        let recurTag = <Tag closeable={false} variant={VARIANT.solid} title={'Notifying ' + group?.name + ' ' + recur.toLocaleLowerCase()}>
            {recur[0].toUpperCase() + recur.substring(1)}
        </Tag>

        let onTag
        if(recur === 'weekly') {
            onTag = <Tag closeable={false} variant={VARIANT.solid} title={'every ' + startAt.toFormat('cccc')}>
                {startAt.toFormat('cccc')}
            </Tag>
        } else if(recur === 'monthly') {
            onTag = <Tag closeable={false} variant={VARIANT.solid} title={'on the ' + startAt.toFormat('d') + ([,'st','nd','rd'][startAt.toFormat('d').match`1?.$`] || 'th') + ' day of each month'}>
                {startAt.toFormat('d') + ([,'st','nd','rd'][startAt.toFormat('d').match`1?.$`] || 'th')}
            </Tag>
        }

        let atTag = <Tag closeable={false} variant={VARIANT.solid} title={'at ' + startAt.toLocaleString(DateTime.TIME_SIMPLE) + ' ' + startAt.offsetNameShort}>
            {startAt.toLocaleString(DateTime.TIME_SIMPLE) + ' ' + startAt.offsetNameShort}
        </Tag>

        return <div className='recurrence-info'>
            {recurTag} {onTag} {atTag}
        </div>
    }

    return(
        <div className='details domain'>
            <Modal
                onClose={() => setDeleting(false)}
                closeable
                isOpen={deleting}
                animate
                autoFocus
                size={MODALSIZE.default}
                role={MODALROLE.dialog}
            >
                <ModalHeader>Delete Domain</ModalHeader>
                <ModalBody>
                    Are you sure you want to delete <em>{group?.name}</em>'s domain <strong>{domain?.name}</strong>?
                </ModalBody>
                <ModalFooter>
                    <ModalButton kind={BUTTONKIND.tertiary} onClick={() => setDeleting(false)}>
                        Cancel
                    </ModalButton>
                    <ModalButton onClick={() => deleteDomain()}>
                        Delete
                    </ModalButton>
                </ModalFooter>
            </Modal>
            <Breadcrumbs>
                <Link to={'/group/' + group?.id}>
                    {group?.name}
                </Link>
                {editing ?
                    <Input
                        value={name}
                        size={INPUTSIZE.mini}
                        onChange={e => setName(e.target.value)}
                        placeholder='Enter a new domain name for this domain'
                        type='text'
                        autoFocus
                        onFocus={() => setEditingSuccess(null)}
                        onBlur={() => changeName()}
                        error={editingSuccess === false}
                        positive={editingSuccess === true}
                    />
                :
                    <>
                        <span onClick={() => setEditing(true)}>{domain?.name}</span>
                        {/* <Tag closeable={false} kind={domain?.active ? TAGKIND.positive : TAGKIND.negative} overrides={{
                            Root: {
                                style: () => ({
                                    fontSize: '0.5em',
                                    marginLeft: '2em',
                                    marginTop: '-2em'
                                })
                            }
                        }}>{domain?.active ? 'Active' : 'Inactive'}</Tag> */}
                    </>
                }
            </Breadcrumbs>
            <ButtonGroup selected={[
                ... recurEditing ? [0] : [],
                ... deleting ? [1] : []
            ]}>
                <Button onClick={() => setRecurEditing(state => !state)}>Change Recurrence</Button>
                <Button onClick={() => setDeleting(state => !state)}>Delete Domain</Button>
            </ButtonGroup>
            <h3>Recurrence</h3>
            <div>
                {
                    recurEditing ?
                        <div className='recurrence-form'>
                            <FormControl label='Frequency'>
                                <ButtonGroup
                                    mode={MODE.radio}
                                    selected={recurRadio}
                                    onClick={(event, index) => {
                                        setRecur(event.target.value)
                                        setRecurRadio(index)
                                    }}
                                >
                                    <Button value='daily'>Daily</Button>
                                    <Button value='weekly'>Weekly</Button>
                                    <Button value='monthly'>Monthly</Button>
                                </ButtonGroup>
                            </FormControl>
                                    <FormControl label='Start Date'>
                                        <DatePicker
                                            value={recurDate}
                                            onChange={({ date }) => setRecurDate(Array.isArray(date) ? date : [date])}
                                        />
                                    </FormControl>
                                    <FormControl label='Email Time'>
                                        <TimePicker
                                            value={recurTime}
                                            onChange={date => setRecurTime(date)}
                                        />
                                    </FormControl>
                                    <FormControl label='Timezone'>
                                        <TimezonePicker
                                            value={recurTz}
                                            onChange={({ id }) => setRecurTz(id)}
                                        />
                                    </FormControl>
                            <ButtonGroup>
                                <Button onClick={() => setRecurEditing(false)}>Cancel</Button>
                                <Button onClick={updateRecur}>Save</Button>
                            </ButtonGroup>
                        </div>
                    :
                    recurrenceInfo()
                }
            </div>
            <h3>Analysis</h3>
            <StyledRoot>
                <StyledTable className='analysis-table'>
                    <StyledTableHead>
                        <StyledTableHeadRow>
                            <StyledTableHeadCell>Found</StyledTableHeadCell>
                            <StyledTableHeadCell>Domain</StyledTableHeadCell>
                            <StyledTableHeadCell>Created</StyledTableHeadCell>
                            <StyledTableHeadCell>IP Address</StyledTableHeadCell>
                        </StyledTableHeadRow>
                    </StyledTableHead>
                    <StyledTableBody>
                        {Data.lookalikes.filter(lookalike => lookalike.domainId === domain?.id).map(lookalike => {
                            let foundOn = DateTime.fromISO(lookalike.foundOn)
                            if(foundOn.year === new Date().getFullYear()) {
                                foundOn = foundOn.toFormat('MMM dd, hh:mm a')
                            } else {
                                foundOn = foundOn.toFormat('y, MMM dd, hh:mm a')
                            }
                            let creationDate = DateTime.fromISO(lookalike.creationDate)
                            if(creationDate.year === new Date().getFullYear()) {
                                creationDate = creationDate.toFormat('MMM dd, hh:mm a')
                            } else {
                                creationDate = creationDate.toFormat('y, MMM dd, hh:mm a')
                            }
                            return(
                                <StyledTableBodyRow key={lookalike.id}>
                                    <StyledTableBodyCell title={DateTime.fromISO(lookalike.foundOn).toFormat('y-LL-dd\nhh:mm:ss.SSS a')}>
                                        {foundOn}
                                    </StyledTableBodyCell>
                                    <StyledTableBodyCell>
                                        {lookalike.name}
                                        {<a href={'https://who.is/whois/' + lookalike.name}>
                                            <Tag 
                                                closeable={false}
                                                kind={TAGKIND.blue}
                                                onClick={() => {}}
                                                overrides={{
                                                    Root: {
                                                        style: ({ $theme }) => ({
                                                            ':hover': {
                                                                backgroundColor: $theme.colors.accent100,
                                                                boxShadow: 'none'
                                                            }
                                                        })
                                                    }
                                                }}
                                            >whois</Tag>
                                        </a>}
                                    </StyledTableBodyCell>
                                    <StyledTableBodyCell title={DateTime.fromISO(lookalike.creationDate).toFormat('y-LL-dd\nhh:mm:ss a')}>
                                        {creationDate}
                                    </StyledTableBodyCell>
                                    <StyledTableBodyCell>
                                        <code>{lookalike.ipAddress}</code>
                                    </StyledTableBodyCell>
                                </StyledTableBodyRow>
                            )
                        })}
                    </StyledTableBody>
                </StyledTable>
            </StyledRoot>
        </div>
    )

}

export default Domain