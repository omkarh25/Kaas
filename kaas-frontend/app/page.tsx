"use client";

import React, { useState, useEffect } from 'react';
import { AssetsTable } from '@/components/ui/AssetsTable';
import { TransactionsTable } from '@/components/ui/TransactionsTable';
import { Asset, Transaction } from '@/types';
import api from '@/lib/api';

export default function Home() {
  const [assets, setAssets] = useState<Asset[]>([]);
  const [transactions, setTransactions] = useState<Transaction[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const assetsResponse = await api.get('/assets/');
        setAssets(assetsResponse.data);

        const transactionsResponse = await api.get('/transactions/');
        setTransactions(transactionsResponse.data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <main className="container mx-auto py-10">
      <h1 className="text-3xl font-bold mb-8">Kaas Dashboard</h1>
      
      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4">Assets</h2>
        <AssetsTable assets={assets} showSlNo={true} />
      </section>

      <section>
        <h2 className="text-2xl font-semibold mb-4">Transactions</h2>
        <TransactionsTable transactions={transactions} showTrNo={true} />
      </section>
    </main>
  );
}