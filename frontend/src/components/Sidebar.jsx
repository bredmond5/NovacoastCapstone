import React, { useEffect, useState } from 'react'
import { Navigation } from 'baseui/side-navigation'
import { useHistory, useLocation, Link } from 'react-router-dom'

import Context from '../Context'
import Data from '../Data.json'

function Sidebar() {

	let history = useHistory()
	let location = useLocation()

	const [groups, setGroups] = useState([])

	useEffect(() => {
		setGroups(Data.groups.sort((a, b) => a.name.localeCompare(b.name)))
	})

	return(
		<div className='sidebar'>
			<Link className='logo' to=''>
				<img 
					src='/assets/logos/novacoast-logo-vector.svg'
					title='Home'
					alt='NC | '
				/>
				<span>DNS TWIST</span>
			</Link>
			<Navigation
				items={[
					{
						title: 'Search',
						itemId: '/search'
					},
					{
						title: 'Groups',
						subNav: [
							{
								title: '+ Add New Group',
								itemId: '/group/add'
							},
							...groups.map(group => {
								return {
									title: group.name,
									itemId: '/group/' + group.id
								}
							}) || []
						]
					}
				]}
				activeItemId={location.pathname}
				onChange={({ event, item }) => {
					// prevent page reload
					event.preventDefault()
					history.push(item.itemId)
				}}
				overrides={{
					Root: {
						style: () => ({
							width: '100%',
							borderTop: '1px solid #444'
						})
					},
					NavItem: {
						style: ({ $level, $active, $selectable }) => {
							let style = {
								fontWeight: 500,
								paddingTop: (16 / $level) + 'px',
								paddingBottom: (16 / $level) + 'px',
								paddingRight: '16px',
								paddingLeft: ($level * 16) + 'px',
								borderBottom: '1px solid #444',
								borderLeftWidth: '0px',
								borderLeftColor: 'transparent'
							}
							if (!$active) {
								style.color = '#eee'
								style.backgroundColor = 'inherit'
								if($selectable) {
									style[':hover'] = { color: '#fff', background: 'rgba(0,0,0,0.1)' }
								}
							} else {
								style.color = '#333'
								style.backgroundColor = 'white'
								style.boxShadow = 'inset 5px 0 0 #FC9A18'
							}
							return style
						}
					},
					SubNavContainer: {
						style: () => ({
							fontSize: '0.9em'
						})
					},
					NavLink: {
						style: () => {
						  return { color: '#333' };
						}
					},
					
				}}
			/>
		</div>
	)

}

export default Sidebar