import React, { useState, useEffect } from 'react';
import axios from 'axios';
import PhilosophyCard from './PhilosophyCard';
import ReligionCard from './ReligionCard';
import AstrologyCard from './AstrologyCard';

function KnowledgeBase() {
    const [activeTab, setActiveTab] = useState('philosophy');
    const [data, setData] = useState({
        philosophies: [],
        religions: [],
        astrologicalSystems: []
    });
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [searchQuery, setSearchQuery] = useState('');

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [philosophies, religions, astrology] = await Promise.all([
                    axios.get('http://localhost:8001/philosophies/'),
                    axios.get('http://localhost:8001/religions/'),
                    axios.get('http://localhost:8001/astrological-systems/')
                ]);

                setData({
                    philosophies: philosophies.data,
                    religions: religions.data,
                    astrologicalSystems: astrology.data
                });
                setLoading(false);
            } catch (err) {
                setError('Failed to fetch data');
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    const handleSearch = async () => {
        if (!searchQuery.trim()) return;
        
        try {
            const response = await axios.get(`http://localhost:8001/search/?query=${searchQuery}`);
            setData({
                philosophies: response.data.philosophies,
                religions: response.data.religions,
                astrologicalSystems: response.data.astrological_systems
            });
        } catch (err) {
            setError('Search failed');
        }
    };

    if (loading) return <div className="text-center mt-5">Loading...</div>;
    if (error) return <div className="text-center mt-5 text-danger">{error}</div>;

    return (
        <div className="container mt-4">
            <h1 className="text-center mb-4">Wisdom Traditions Database</h1>
            
            {/* Search Bar */}
            <div className="row mb-4">
                <div className="col-md-8 mx-auto">
                    <div className="input-group">
                        <input
                            type="text"
                            className="form-control"
                            placeholder="Search across all traditions..."
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                        />
                        <button 
                            className="btn btn-primary"
                            onClick={handleSearch}
                        >
                            Search
                        </button>
                    </div>
                </div>
            </div>

            {/* Navigation Tabs */}
            <ul className="nav nav-tabs mb-4">
                <li className="nav-item">
                    <button 
                        className={`nav-link ${activeTab === 'philosophy' ? 'active' : ''}`}
                        onClick={() => setActiveTab('philosophy')}
                    >
                        Philosophy
                    </button>
                </li>
                <li className="nav-item">
                    <button 
                        className={`nav-link ${activeTab === 'religion' ? 'active' : ''}`}
                        onClick={() => setActiveTab('religion')}
                    >
                        Religion
                    </button>
                </li>
                <li className="nav-item">
                    <button 
                        className={`nav-link ${activeTab === 'astrology' ? 'active' : ''}`}
                        onClick={() => setActiveTab('astrology')}
                    >
                        Astrology
                    </button>
                </li>
            </ul>

            {/* Content */}
            <div className="row">
                {activeTab === 'philosophy' && (
                    data.philosophies.map(philosophy => (
                        <div key={philosophy.id} className="col-md-6 mb-4">
                            <PhilosophyCard philosophy={philosophy} />
                        </div>
                    ))
                )}
                
                {activeTab === 'religion' && (
                    data.religions.map(religion => (
                        <div key={religion.id} className="col-md-6 mb-4">
                            <ReligionCard religion={religion} />
                        </div>
                    ))
                )}
                
                {activeTab === 'astrology' && (
                    data.astrologicalSystems.map(system => (
                        <div key={system.id} className="col-md-6 mb-4">
                            <AstrologyCard system={system} />
                        </div>
                    ))
                )}
            </div>
        </div>
    );
}

export default KnowledgeBase;