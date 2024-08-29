'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { axiosAuth, isAuthenticated, logout } from '@/utils/auth';

interface Asset {
  id: number;
  name: string;
  amount: number;
  department: string;
  comments: string;
}

export default function AssetsPage() {
  const [assets, setAssets] = useState<Asset[]>([]);
  const [newAsset, setNewAsset] = useState<Omit<Asset, 'id'>>({
    name: '',
    amount: 0,
    department: '',
    comments: '',
  });
  const [sortBy, setSortBy] = useState<string>('id');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc');
  const [filterName, setFilterName] = useState<string>('');
  const [filterDepartment, setFilterDepartment] = useState<string>('');
  const router = useRouter();

  useEffect(() => {
    if (!isAuthenticated()) {
      router.push('/login');
    } else {
      fetchAssets();
    }
  }, [router, sortBy, sortOrder, filterName, filterDepartment]);

  const fetchAssets = async () => {
    try {
      const response = await axiosAuth.get('/assets/', {
        params: {
          sort_by: sortBy,
          sort_order: sortOrder,
          name: filterName,
          department: filterDepartment,
        },
      });
      setAssets(response.data);
    } catch (error) {
      console.error('Error fetching assets:', error);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setNewAsset((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await axiosAuth.post('/assets/', newAsset);
      fetchAssets();
      setNewAsset({ name: '', amount: 0, department: '', comments: '' });
    } catch (error) {
      console.error('Error creating asset:', error);
    }
  };

  const handleSort = (column: string) => {
    if (sortBy === column) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortBy(column);
      setSortOrder('asc');
    }
  };

  const handleLogout = () => {
    logout();
    router.push('/login');
  };

  return (
    <div className="container mx-auto p-4">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Assets</h1>
        <button onClick={handleLogout} className="bg-red-500 text-white p-2 rounded">Logout</button>
      </div>
      
      <form onSubmit={handleSubmit} className="mb-4">
        <input
          type="text"
          name="name"
          value={newAsset.name}
          onChange={handleInputChange}
          placeholder="Asset Name"
          className="mr-2 p-2 border"
        />
        <input
          type="number"
          name="amount"
          value={newAsset.amount}
          onChange={handleInputChange}
          placeholder="Amount"
          className="mr-2 p-2 border"
        />
        <input
          type="text"
          name="department"
          value={newAsset.department}
          onChange={handleInputChange}
          placeholder="Department"
          className="mr-2 p-2 border"
        />
        <input
          type="text"
          name="comments"
          value={newAsset.comments}
          onChange={handleInputChange}
          placeholder="Comments"
          className="mr-2 p-2 border"
        />
        <button type="submit" className="bg-blue-500 text-white p-2 rounded">Add Asset</button>
      </form>

      <div className="mb-4">
        <input
          type="text"
          value={filterName}
          onChange={(e) => setFilterName(e.target.value)}
          placeholder="Filter by name"
          className="mr-2 p-2 border"
        />
        <input
          type="text"
          value={filterDepartment}
          onChange={(e) => setFilterDepartment(e.target.value)}
          placeholder="Filter by department"
          className="mr-2 p-2 border"
        />
      </div>
      
      <table className="w-full border-collapse border">
        <thead>
          <tr className="bg-gray-200">
            <th className="border p-2 cursor-pointer" onClick={() => handleSort('name')}>
              Name {sortBy === 'name' && (sortOrder === 'asc' ? '▲' : '▼')}
            </th>
            <th className="border p-2 cursor-pointer" onClick={() => handleSort('amount')}>
              Amount {sortBy === 'amount' && (sortOrder === 'asc' ? '▲' : '▼')}
            </th>
            <th className="border p-2 cursor-pointer" onClick={() => handleSort('department')}>
              Department {sortBy === 'department' && (sortOrder === 'asc' ? '▲' : '▼')}
            </th>
            <th className="border p-2">Comments</th>
          </tr>
        </thead>
        <tbody>
          {assets.map((asset) => (
            <tr key={asset.id}>
              <td className="border p-2">{asset.name}</td>
              <td className="border p-2">{asset.amount}</td>
              <td className="border p-2">{asset.department}</td>
              <td className="border p-2">{asset.comments}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}