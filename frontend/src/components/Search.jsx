import React, { useState, useEffect, useRef, useContext } from 'react'
import { useHistory } from 'react-router-dom'

import { Select, TYPE } from 'baseui/select'

import Context from '../Context'
import Data from '../Data.json'

function Search(props) {

    let history = useHistory()

    const context = useContext(Context)

    const [inputValue, setInputValue] = useState('')
    const [options, setOptions] = useState({
        Groups: [],
        Domains: []
    })

    useEffect(() => {
        async function getOptions() {
            setOptions({
                Groups: Data.groups.filter(g => g.name.toLowerCase().includes(inputValue.toLowerCase())),
                Domains: Data.domains.filter(d => d.name.toLowerCase().includes(inputValue.toLowerCase()))
            })
        }
        const timer = setTimeout(() => {
            if(inputValue) {
                getOptions()
            } else {
                setOptions({ Groups: [], Domains: [] })
            }
        }, 250)
        return () => clearTimeout(timer)
    }, [inputValue])

    useEffect(() => {
        console.log(options)
    }, [options])

    return(
        <div className='search'>
            <h1>Search</h1>
            <Select
                autoFocus
                placeholder='Search groups and domains'
                options={options}
                onChange={({ value }) => history.push(value[0].groupId ? ('/domain/' + value[0].id) : ('/group/' + value[0].id))}
                type={TYPE.search}
                maxDropdownHeight='90vh'
                onInputChange={e => setInputValue(e.target.value)}
                labelKey='name'
                getValueLabel={option => option.groupId ? ('/domain/' + option.id) : ('/group/' + option.id)}
            />
        </div>
    )

}

export default Search