import React from 'react'
import { DateTime } from 'luxon'

import { Table } from 'baseui/table-semantic'

import Data from '../Data.json'

function Dashboard(props) {    

    return(
        <div className='dashboard'>
            <h1>Dashboard</h1>
            <Table
                columns={['Domain', 'Group', 'Last Emailed', 'Last Scanned', 'Next Scan']}
                data={Data.domains.filter(domain => domain.active).map(domain => {
                    let nextScan = { days: 1 }
                    if(domain.recur === 'weekly') nextScan = { weeks: 1 }
                    else if(domain.recur === 'monthly') nextScan = { months: 1 }
                    return [
                        domain.name,
                        Data.groups.find(group => group.id === domain.groupId)?.name,
                        // DateTime.fromISO(domain.lastEmailed).toFormat('MMM dd, hh:mma'),
                        // DateTime.fromISO(domain.lastScanned).toFormat('MMM dd, hh:mma'),
                        // DateTime.fromISO(domain.lastScanned).plus(nextScan).toFormat('MMM dd, hh:mma'),
                        'Jan 01, 08:00am',
                        'Jan 01, 07:45am',
                        'Jan 02, 07:45am',
                    ]
                })}
            />
        </div>
    )

}

export default Dashboard