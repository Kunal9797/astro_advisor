import React from 'react';

function AstrologyCard({ system }) {
    return (
        <div className="card h-100 shadow-sm">
            <div className="card-body">
                <h3 className="card-title">{system.name}</h3>
                <h6 className="card-subtitle mb-2 text-muted">Origin: {system.origin}</h6>
                <p className="card-text">{system.description}</p>
                <div className="row mt-3">
                    <div className="col-md-6">
                        <h6>Key Concepts:</h6>
                        <ul className="list-group list-group-flush">
                            {system.key_concepts.map((concept, index) => (
                                <li key={index} className="list-group-item">{concept}</li>
                            ))}
                        </ul>
                    </div>
                    <div className="col-md-6">
                        <h6>Zodiac Signs:</h6>
                        <ul className="list-group list-group-flush">
                            {system.zodiac_signs.map((sign, index) => (
                                <li key={index} className="list-group-item">{sign}</li>
                            ))}
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default AstrologyCard;