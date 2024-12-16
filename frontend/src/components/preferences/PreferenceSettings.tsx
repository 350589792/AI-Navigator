import React, { useState, useEffect } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Badge } from '@/components/ui/badge';
import { X } from 'lucide-react';
import axios from 'axios';
import { API_URL } from '@/config';

interface Category {
  id: number;
  name: string;
}

interface Preference {
  id: number;
  category_id: number;
  keywords: string[];
  schedule_time: string;
  timezone: string;
}

export const PreferenceSettings: React.FC = () => {
  const [categories, setCategories] = useState<Category[]>([]);
  const [selectedCategories, setSelectedCategories] = useState<number[]>([]);
  const [keywords, setKeywords] = useState<string[]>([]);
  const [newKeyword, setNewKeyword] = useState('');
  const [scheduleTime, setScheduleTime] = useState('09:00');
  const [timezone, setTimezone] = useState(Intl.DateTimeFormat().resolvedOptions().timeZone);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Load categories and user preferences
    const fetchData = async () => {
      try {
        const [categoriesRes, preferencesRes] = await Promise.all([
          axios.get(`${API_URL}/categories`),
          axios.get(`${API_URL}/preferences`)
        ]);

        setCategories(categoriesRes.data);

        // Set existing preferences
        const prefs = preferencesRes.data;
        if (prefs) {
          setSelectedCategories(prefs.categories.map((c: any) => c.id));
          setKeywords(prefs.keywords || []);
          setScheduleTime(prefs.schedule_time || '09:00');
          setTimezone(prefs.timezone || Intl.DateTimeFormat().resolvedOptions().timeZone);
        }
      } catch (err) {
        setError('Failed to load preferences');
      }
    };
    fetchData();
  }, []);

  const handleAddKeyword = () => {
    if (newKeyword && !keywords.includes(newKeyword)) {
      setKeywords([...keywords, newKeyword]);
      setNewKeyword('');
    }
  };

  const handleRemoveKeyword = (keyword: string) => {
    setKeywords(keywords.filter((k) => k !== keyword));
  };

  const handleToggleCategory = (categoryId: number) => {
    setSelectedCategories((prev) =>
      prev.includes(categoryId)
        ? prev.filter((id) => id !== categoryId)
        : [...prev, categoryId]
    );
  };

  const handleSavePreferences = async () => {
    try {
      await axios.post(`${API_URL}/preferences`, {
        categories: selectedCategories,
        keywords,
        schedule_time: scheduleTime,
        timezone
      });
      setError(null);
    } catch (err) {
      setError('Failed to save preferences');
    }
  };

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold">Subscription Preferences</h2>

      {/* Category Selection */}
      <div className="space-y-2">
        <Label>Categories</Label>
        <div className="grid grid-cols-4 gap-4">
          {categories.map((category) => (
            <Card
              key={category.id}
              className={`cursor-pointer ${
                selectedCategories.includes(category.id) ? 'border-primary' : ''
              }`}
              onClick={() => handleToggleCategory(category.id)}
            >
              <CardContent className="p-4">
                <h3 className="font-semibold">{category.name}</h3>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Keywords */}
      <div className="space-y-2">
        <Label>Keywords</Label>
        <div className="flex gap-2">
          <Input
            value={newKeyword}
            onChange={(e) => setNewKeyword(e.target.value)}
            placeholder="Enter keyword"
            onKeyPress={(e) => e.key === 'Enter' && handleAddKeyword()}
          />
          <Button onClick={handleAddKeyword}>Add</Button>
        </div>
        <div className="flex flex-wrap gap-2 mt-2">
          {keywords.map((keyword) => (
            <Badge key={keyword} variant="secondary">
              {keyword}
              <X
                className="w-3 h-3 ml-1 cursor-pointer"
                onClick={() => handleRemoveKeyword(keyword)}
              />
            </Badge>
          ))}
        </div>
      </div>

      {/* Schedule Settings */}
      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label htmlFor="scheduleTime">Report Time</Label>
          <Input
            id="scheduleTime"
            type="time"
            value={scheduleTime}
            onChange={(e) => setScheduleTime(e.target.value)}
          />
        </div>

        <div className="space-y-2">
          <Label htmlFor="timezone">Timezone</Label>
          <select
            id="timezone"
            className="w-full p-2 border rounded"
            value={timezone}
            onChange={(e) => setTimezone(e.target.value)}
          >
            {Intl.supportedValuesOf('timeZone').map((tz) => (
              <option key={tz} value={tz}>
                {tz}
              </option>
            ))}
          </select>
        </div>
      </div>

      <Button onClick={handleSavePreferences} className="w-full">
        Save Preferences
      </Button>

      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}
    </div>
  );
};
