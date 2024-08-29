'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { axiosAuth, isAuthenticated, logout } from '@/utils/auth';

interface Transaction {
  id: number;
  date: string;
  description: string;
  amount: number;
  payment_mode: string;
  acc_id: string;
  department: string;
  comments: string | null;
  category: string;
  payment_mode_detail: string;
  zoho_match: boolean;
}

export default function TransactionsPage() {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [newTransaction, setNewTransaction] = useState<Omit<Transaction, 'id'>>({
    date: new Date().toISOString().split('T')[0],
    description: '',
    amount: 0,
    payment_mode: '',
    acc_id: '',
    department: '',
    comments: '',
    category: '',
    payment_mode_detail: '',
    zoho_match: false,
  });
  const [sortBy, setSortBy] = useState<string>('date');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');
  const [filterStartDate, setFilterStartDate] = useState<string>('');
  const [filterEndDate, setFilterEndDate] = useState<string>('');
  const [filterCategory, setFilterCategory] = useState<string>('');
  const [filterDepartment, setFilterDepartment] = useState<string>('');
  const router = useRouter();

  useEffect(() => {
    if (!isAuthenticated()) {
      router.push('/login');
    } else {
      fetchTransactions();
    }
  }, [router, sortBy, sortOrder, filterStartDate, filterEndDate, filterCategory, filterDepartment]);

  const fetchTransactions = async () => {
    try {
      const response = await axiosAuth.get('/transactions/', {
        params: {
          sort_by: sortBy,
          sort_order: sortOrder,
          start_date: filterStartDate,
          end_date: filterEndDate,
          category: filterCategory,
          department: filterDepartment,
        },
      });
      setTransactions(response.data);
    } catch (error) {
      console.error('Error fetching transactions:', error);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    setNewTransaction((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? (e.target as HTMLInputElement).checked : value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await axiosAuth.post('/transactions/', newTransaction);
      fetchTransactions();
      setNewTransaction({
        date: new Date().toISOString().split('T')[0],
        description: '',
        amount: 0,
        payment_mode: '',
        acc_id: '',
        department: '',
        comments: '',
        category: '',
        payment_mode_detail: '',
        zoho_match: false,
      });
    } catch (error) {
      console.error('Error creating transaction:', error);
    }
  };

  const handleSort = (column: string) => {
    if (sortBy === column) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortBy(column);
      setSortOrder('desc');
    }
  };

  const handleLogout = () => {
    logout();
    router.push('/login');
  };

  return (
    <div className="container mx-auto p-4">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Transactions</h1>
        <button onClick={handleLogout} className="bg-red-500 text-white p-2 rounded">Logout</button>
      </div>
      
      <form onSubmit={handleSubmit} className="mb-4 space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <input
            type="date"
            name="date"
            value={newTransaction.date}
            onChange={handleInputChange}
            className="p-2 border rounded"
            required
          />
          <input
            type="text"
            name="description"
            value={newTransaction.description}
            onChange={handleInputChange}
            placeholder="Description"
            className="p-2 border rounded"
            required
          />
          <input
            type="number"
            name="amount"
            value={newTransaction.amount}
            onChange={handleInputChange}
            placeholder="Amount"
            className="p-2 border rounded"
            required
          />
          <input
            type="text"
            name="payment_mode"
            value={newTransaction.payment_mode}
            onChange={handleInputChange}
            placeholder="Payment Mode"
            className="p-2 border rounded"
            required
          />
          <input
            type="text"
            name="acc_id"
            value={newTransaction.acc_id}
            onChange={handleInputChange}
            placeholder="Account ID"
            className="p-2 border rounded"
            required
          />
          <input
            type="text"
            name="department"
            value={newTransaction.department}
            onChange={handleInputChange}
            placeholder="Department"
            className="p-2 border rounded"
            required
          />
          <input
            type="text"
            name="comments"
            value={newTransaction.comments || ''}
            onChange={handleInputChange}
            placeholder="Comments"
            className="p-2 border rounded"
          />
          <input
            type="text"
            name="category"
            value={newTransaction.category}
            onChange={handleInputChange}
            placeholder="Category"
            className="p-2 border rounded"
            required
          />
          <input
            type="text"
            name="payment_mode_detail"
            value={newTransaction.payment_mode_detail}
            onChange={handleInputChange}
            placeholder="Payment Mode Detail"
            className="p-2 border rounded"
            required
          />
          <div className="flex items-center">
            <input
              type="checkbox"
              name="zoho_match"
              checked={newTransaction.zoho_match}
              onChange={handleInputChange}
              className="mr-2"
            />
            <label htmlFor="zoho_match">Zoho Match</label>
          </div>
        </div>
        <button type="submit" className="bg-blue-500 text-white p-2 rounded w-full">Add Transaction</button>
      </form>

      <div className="mb-4 flex space-x-2">
        <input
          type="date"
          value={filterStartDate}
          onChange={(e) => setFilterStartDate(e.target.value)}
          className="p-2 border rounded"
          placeholder="Start Date"
        />
        <input
          type="date"
          value={filterEndDate}
          onChange={(e) => setFilterEndDate(e.target.value)}
          className="p-2 border rounded"
          placeholder="End Date"
        />
        <input
          type="text"
          value={filterCategory}
          onChange={(e) => setFilterCategory(e.target.value)}
          className="p-2 border rounded"
          placeholder="Filter by Category"
        />
        <input
          type="text"
          value={filterDepartment}
          onChange={(e) => setFilterDepartment(e.target.value)}
          className="p-2 border rounded"
          placeholder="Filter by Department"
        />
      </div>
      
      <table className="w-full border-collapse border">
        <thead>
          <tr className="bg-gray-200">
            <th className="border p-2 cursor-pointer" onClick={() => handleSort('date')}>
              Date {sortBy === 'date' && (sortOrder === 'asc' ? '▲' : '▼')}
            </th>
            <th className="border p-2 cursor-pointer" onClick={() => handleSort('description')}>
              Description {sortBy === 'description' && (sortOrder === 'asc' ? '▲' : '▼')}
            </th>
            <th className="border p-2 cursor-pointer" onClick={() => handleSort('amount')}>
              Amount {sortBy === 'amount' && (sortOrder === 'asc' ? '▲' : '▼')}
            </th>
            <th className="border p-2">Payment Mode</th>
            <th className="border p-2">Account ID</th>
            <th className="border p-2 cursor-pointer" onClick={() => handleSort('department')}>
              Department {sortBy === 'department' && (sortOrder === 'asc' ? '▲' : '▼')}
            </th>
            <th className="border p-2 cursor-pointer" onClick={() => handleSort('category')}>
              Category {sortBy === 'category' && (sortOrder === 'asc' ? '▲' : '▼')}
            </th>
            <th className="border p-2">Zoho Match</th>
          </tr>
        </thead>
        <tbody>
          {transactions.map((transaction) => (
            <tr key={transaction.id}>
              <td className="border p-2">{new Date(transaction.date).toLocaleDateString()}</td>
              <td className="border p-2">{transaction.description}</td>
              <td className="border p-2">{transaction.amount}</td>
              <td className="border p-2">{transaction.payment_mode}</td>
              <td className="border p-2">{transaction.acc_id}</td>
              <td className="border p-2">{transaction.department}</td>
              <td className="border p-2">{transaction.category}</td>
              <td className="border p-2">{transaction.zoho_match ? 'Yes' : 'No'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}