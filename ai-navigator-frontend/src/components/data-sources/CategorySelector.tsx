import React, { useState, useEffect } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Plus } from 'lucide-react';
import axios from 'axios';
import { API_BASE_URL } from '@/config';

interface Category {
  id: number;
  name: string;
  description: string;
}

interface DataSource {
  id: number;
  name: string;
  url: string;
  type: 'preset' | 'custom';
  description?: string;
}

export const CategorySelector: React.FC = () => {
  const [categories, setCategories] = useState<Category[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<number | null>(null);
  const [dataSources, setDataSources] = useState<DataSource[]>([]);
  const [customUrl, setCustomUrl] = useState('');
  const [customName, setCustomName] = useState('');
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Load categories
    const fetchCategories = async () => {
      try {
        const response = await axios.get<Category[]>(`${API_BASE_URL}/categories`);
        setCategories(response.data);
      } catch {
        setError('Failed to load categories');
      }
    };
    fetchCategories();
  }, []);

  useEffect(() => {
    // Load data sources for selected category
    if (selectedCategory) {
      const fetchDataSources = async () => {
        try {
          const response = await axios.get<DataSource[]>(
            `${API_BASE_URL}/data-sources/category/${selectedCategory}`
          );
          setDataSources(response.data);
        } catch {
          setError('Failed to load data sources');
        }
      };
      fetchDataSources();
    }
  }, [selectedCategory]);

  const handleAddCustomSource = async () => {
    if (!selectedCategory) {
      setError('Please select a category first');
      return;
    }

    try {
      await axios.post(`${API_BASE_URL}/data-sources`, {
        name: customName,
        url: customUrl,
        category_id: selectedCategory
      });

      // Refresh data sources
      const response = await axios.get<DataSource[]>(
        `${API_BASE_URL}/data-sources/category/${selectedCategory}`
      );
      setDataSources(response.data);

      // Clear form
      setCustomUrl('');
      setCustomName('');
      setError(null);
    } catch {
      setError('Failed to add custom source');
    }
  };

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold">Data Sources</h2>

      {/* Category Selection */}
      <div className="grid grid-cols-4 gap-4">
        {categories.map((category) => (
          <Card
            key={category.id}
            className={`cursor-pointer ${
              selectedCategory === category.id ? 'border-primary' : ''
            }`}
            onClick={() => setSelectedCategory(category.id)}
          >
            <CardContent className="p-4">
              <h3 className="font-semibold">{category.name}</h3>
              <p className="text-sm text-muted-foreground">
                {category.description}
              </p>
            </CardContent>
          </Card>
        ))}
      </div>

      {selectedCategory && (
        <Tabs defaultValue="preset" className="w-full">
          <TabsList>
            <TabsTrigger value="preset">Preset Sources</TabsTrigger>
            <TabsTrigger value="custom">Add Custom Source</TabsTrigger>
          </TabsList>

          <TabsContent value="preset">
            <div className="grid grid-cols-3 gap-4">
              {dataSources
                .filter((source) => source.type === 'preset')
                .map((source) => (
                  <Card key={source.id}>
                    <CardContent className="p-4">
                      <h4 className="font-semibold">{source.name}</h4>
                      <p className="text-sm text-muted-foreground">
                        {source.description}
                      </p>
                      <a
                        href={source.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-sm text-primary hover:underline"
                      >
                        Visit Source
                      </a>
                    </CardContent>
                  </Card>
                ))}
            </div>
          </TabsContent>

          <TabsContent value="custom">
            <Card>
              <CardContent className="p-4 space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="sourceName">Source Name</Label>
                  <Input
                    id="sourceName"
                    value={customName}
                    onChange={(e) => setCustomName(e.target.value)}
                    placeholder="Enter source name"
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="sourceUrl">Source URL</Label>
                  <Input
                    id="sourceUrl"
                    value={customUrl}
                    onChange={(e) => setCustomUrl(e.target.value)}
                    placeholder="https://"
                  />
                </div>

                <Button
                  onClick={handleAddCustomSource}
                  className="w-full"
                  disabled={!customName || !customUrl}
                >
                  <Plus className="w-4 h-4 mr-2" />
                  Add Custom Source
                </Button>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      )}

      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}
    </div>
  );
};
