"use client";
import React from "react";
import dynamic from 'next/dynamic'

export default function Map() {
    const Map = React.useMemo(() => dynamic(
      () => import('./MapComponent'),
      { 
        loading: () => <p>A map is loading</p>,
        ssr: false
      }
    ), [])
  
    return <div>
      <Map />
    </div>
  }