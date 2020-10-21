import React from 'react'
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom'
import { Client as Styletron } from 'styletron-engine-atomic'
import { Provider as StyletronProvider } from 'styletron-react'
import { LightTheme, BaseProvider } from 'baseui'
import { Block } from 'baseui/block'
import axios from 'axios'

import './App.scss'
import Context from './Context'
import Sidebar from './components/Sidebar'
import Main from './components/Main'
import Dashboard from './components/Dashboard'
import Search from './components/Search'
import AddGroup from './components/AddGroup'
import Group from './components/Group'
import Domain from './components/Domain'

const engine = new Styletron()

function App() {
	return (
		<StyletronProvider value={engine}>
      		<BaseProvider theme={LightTheme}>
				<Router basename={process.env.PUBLIC_URL}>
					<Context.Provider value={{
						backend: axios.create({
							baseURL: 'http://localhost:5000'
						})
					}}>
						<Block className='base-block'>
							<Sidebar/>
							<Main>
								<Switch>
									<Route exact path='/' render={(props) => <Dashboard {...props} />}/>
									<Route path='/search' render={(props) => <Search {...props} />}/>
									<Route path='/group/add' render={(props) => <AddGroup {...props} />}/>
									<Route path='/group/:id' render={(props) => <Group {...props} />}/>
									<Route path='/domain/:id' render={(props) => <Domain {...props} />}/>
								</Switch>
							</Main>
						</Block>
					</Context.Provider>
				</Router>
			</BaseProvider>
		</StyletronProvider>
	)
}

export default App
