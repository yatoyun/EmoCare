
import React, { useEffect, useState } from 'react'
import api from '../configs/api'

function Statistics() {
  const [stats, setStats] = useState(null)

  useEffect(() => {
    api.get('user-stats/')
      .then((response) => setStats(response.data))
      .catch((error) => console.error('Error fetching user stats:', error))
  }, [])

  if (!stats) {
    return <div>Loading statistics...</div>
  }

  return (
    <div className="max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">Your Mood Statistics</h2>
      <div className="bg-white rounded-lg shadow-md p-4">
        <div className="mb-4">
          <h3 className="text-lg font-semibold">Overall Mood</h3>
          <p className="text-3xl font-bold">{stats.overallMood}</p>
        </div>
        <div className="mb-4">
          <h3 className="text-lg font-semibold">Depression Level</h3>
          <p className="text-3xl font-bold">{stats.depressionLevel}</p>
        </div>
        <div>
          <h3 className="text-lg font-semibold">Mood History</h3>
          {/* Here you can add a chart or graph to visualize mood history */}
          <p>Mood history visualization to be implemented</p>
        </div>
      </div>
    </div>
  )
}

export default Statistics

